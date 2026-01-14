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


def link_not_found_handler(request: Request, exc: LinkNotFound) -> JSONResponse:
    """Handler for LinkNotFound exception"""
    logger.warning(f"Link not found: {str(exc)} - Path: {request.url.path}")

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": str(exc) if str(exc) else "Link not found",
            "error_type": "link_not_found",
        },
    )


def db_exception_handler(request: Request, exc: DbException) -> JSONResponse:
    """Handler for database exceptions"""
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


def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handler for general application exceptions"""
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
