from datetime import datetime
from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.core.config import config
from app.core.logger import get_logger
from app.api.link import router
from app.services.link import LinkService
from app.models.input import SortIDInput
from app.db.init import SessionDep
from app.core.exception import (
    DbException,
    db_exception_handler,
    AppException,
    app_exception_handler,
    LinkNotFound,
    link_not_found_handler,
)

logger = get_logger(__name__)

app = FastAPI(
    title="Shorty",
    version="0.0.1",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    docs_url=None if config.env == "production" else "/docs",
    redoc_url=None if config.env == "production" else "/redoc",
    openapi_url=None if config.env == "production" else "/openapi.json",
)

templates = Jinja2Templates(directory="app/templates")

# register the exceptions
app.add_exception_handler(DbException, db_exception_handler)
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(LinkNotFound, link_not_found_handler)


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle unhandled exceptions by logging and rendering the 404 page.

    Args:
        request (Request): The incoming HTTP request.
        exc (Exception): The unhandled exception.

    Returns:
        TemplateResponse: Rendered 404.html template with current year.
    """
    logger.critical(
        f"Unhandled exception: {str(exc)} - Path: {request.url.path}", exc_info=True
    )
    return templates.TemplateResponse(
        "404.html",
        {"request": request, "year": datetime.now().year},
    )


# register routers
app.include_router(router=router)


# root level routes
@app.get("/", status_code=status.HTTP_200_OK)
async def handle_home_page(request: Request):
    """
    Render the home page with the URL shortening form.

    Args:
        request (Request): The incoming HTTP request.

    Returns:
        TemplateResponse: Rendered home.html template with current year.
    """
    return templates.TemplateResponse(
        "home.html", {"request": request, "year": datetime.now().year}
    )


@app.get("/404", status_code=status.HTTP_404_NOT_FOUND)
async def handle_404_page(request: Request):
    """
    Render the 404 error page for invalid short URLs.

    Args:
        request (Request): The incoming HTTP request.

    Returns:
        TemplateResponse: Rendered 404.html template with current year.
    """
    return templates.TemplateResponse(
        "404.html", {"request": request, "year": datetime.now().year}
    )


@app.get("/{short_id}")
async def redirect_short_id(short_id: str, session: SessionDep):
    """
    Redirect to the original URL for a given short ID.

    Validates the short ID, retrieves the original URL from the database,
    and performs a permanent redirect.

    Args:
        short_id (str): The short ID to redirect from.
        session (SessionDep): Database session dependency.

    Returns:
        RedirectResponse: HTTP 301 redirect to the original URL or 404 page.

    Raises:
        ValidationError: If the short ID format is invalid.
    """
    id_input = SortIDInput(sort_id=short_id)
    link_service = LinkService(session=session)
    original_url = link_service.get_original_link(sort_id=id_input.sort_id)
    return RedirectResponse(
        url=original_url, status_code=status.HTTP_301_MOVED_PERMANENTLY
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app", host="0.0.0.0", port=9000, log_level="info", reload=True
    )
