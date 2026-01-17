import time
from functools import wraps
from typing import Callable, Any, Dict, List
from fastapi import Request, HTTPException, status
from app.core.logger import get_logger

logger = get_logger(__name__)

# In-memory storage for rate limiting
_rate_limit_storage: Dict[str, List[float]] = {}


def get_identifier(request: Request) -> str:
    """Get client identifier (IP address)."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0]
    return request.client.host if request.client else "unknown"


def rate_limit(times: int, seconds: int):
    """
    Decorator for rate limiting endpoints using in-memory storage.
    
    Args:
        times: Number of allowed requests
        seconds: Time window in seconds
    
    Usage:
        @app.post("/login")
        @rate_limit(times=5, seconds=60)
        def login(request: Request, ...):
            pass
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Find the Request object
            request = None
            
            # Check in kwargs first
            if "request" in kwargs:
                request = kwargs["request"]
            else:
                # Check in positional args
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break
            
            if not request:
                raise ValueError(
                    f"Request object not found in {func.__name__}. "
                    "Make sure to include 'request: Request' parameter."
                )
            
            # Get client identifier
            identifier = get_identifier(request)
            
            # Create a unique key for this endpoint and client
            key = f"{func.__name__}:{identifier}"
            
            # Get current timestamp
            now = time.time()
            
            # Initialize storage for this key if needed
            if key not in _rate_limit_storage:
                _rate_limit_storage[key] = []
            
            # Get timestamps for this key
            timestamps = _rate_limit_storage[key]
            
            # Remove timestamps older than the time window
            timestamps[:] = [t for t in timestamps if now - t < seconds]
            
            # Check if limit exceeded
            if len(timestamps) >= times:
                # Calculate retry-after time
                oldest_timestamp = timestamps[0]
                retry_after = int(seconds - (now - oldest_timestamp)) + 1
                
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail={
                        "error": "Rate limit exceeded",
                        "message": f"Too many requests. Try again in {retry_after} seconds.",
                        "retry_after": retry_after
                    },
                    headers={"Retry-After": str(retry_after)}
                )
            
            # Add current timestamp
            timestamps.append(now)
            
            # Cleanup old keys periodically (every 100 requests)
            if len(_rate_limit_storage) % 100 == 0:
                _cleanup_old_entries(seconds)
            
            # Call the original function (no await)
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


def _cleanup_old_entries(window: int):
    """Remove entries that are completely expired."""
    now = time.time()
    keys_to_delete = []
    
    for key, timestamps in _rate_limit_storage.items():
        # Remove old timestamps
        timestamps[:] = [t for t in timestamps if now - t < window]
        
        # Mark empty entries for deletion
        if not timestamps:
            keys_to_delete.append(key)
    
    # Delete empty entries
    for key in keys_to_delete:
        del _rate_limit_storage[key]
    
    if keys_to_delete:
        logger.debug(f"Cleaned up {len(keys_to_delete)} expired rate limit entries")


