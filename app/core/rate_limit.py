import hashlib
import time
from functools import wraps
from fastapi import HTTPException, Request
from typing import Any, Callable


def rate_limit(max_calls: int, period: int):
    def decorator(func: Callable[[Request], Any]) -> Callable[[Request], Any]:
        usage: dict[str, list[float]] = {}

        @wraps(func)
        def wrapper(request: Request) -> Any:
            if not request.client:
                raise ValueError("Reuest has no client information")

            ip_address: str = request.client.host
            unique_id: str = hashlib.sha256((ip_address).encode()).hexdigest()

            now = time.time()
            if unique_id not in usage:
                usage[unique_id] = []
            timestamps = usage[unique_id]
            timestamps[:] = [t for t in timestamps if now - t < period]

            if len(timestamps) < max_calls:
                timestamps.append(now)
                return func(request)

            wait = period - (now - timestamps[0])
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded. Retry after {wait:.2f} seconds",
            )

        return wrapper

    return decorator
