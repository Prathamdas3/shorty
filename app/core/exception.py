from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.core.logger import get_logger

logger = get_logger(__name__)


class AppException(Exception):
    """Base exception for the application"""
    pass


class LinkNotFound(AppException):
    """Raised when link is not found"""
    pass


class DbException(AppException):
    """Raised when an db error gets"""
    pass


def link_not_found_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handler for LinkNotFound exception"""
    # Type narrowing - we know it's LinkNotFound at runtime
    assert isinstance(exc, LinkNotFound)
    
    logger.warning(f"Link not found: {str(exc)} - Path: {request.url.path}")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": str(exc) if str(exc) else "Link not found",
            "error_type": "link_not_found",
        },
    )


def db_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handler for database exceptions"""
    # Type narrowing - we know it's DbException at runtime
    assert isinstance(exc, DbException)
    
    logger.error(
        f"Database error: {str(exc)} - Path: {request.url.path}", exc_info=True
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "A database error occurred. Please try again later.",
            "error_type": "database_error",
        },
    )


def app_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handler for general application exceptions"""
    # Type narrowing - we know it's AppException at runtime
    assert isinstance(exc, AppException)
    
    logger.error(
        f"Application error: {str(exc)} - Path: {request.url.path}", exc_info=True
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An unexpected error occurred. Please try again later.",
            "error_type": "application_error",
        },
    )