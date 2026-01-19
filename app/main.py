from datetime import datetime
from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles

from app.core.template import templates
from app.core.config import config
from app.core.logger import get_logger
from app.api.router import api_router
from app.web.router import web_router

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


app.mount("/static", StaticFiles(directory="app/static"), name="static")

# register the exceptions
app.add_exception_handler(DbException, db_exception_handler)
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(LinkNotFound, link_not_found_handler)


@app.exception_handler(Exception)
def general_exception_handler(request: Request, exc: Exception):
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
        {"request": request, "year": datetime.now().year, "config": config},
        status_code=status.HTTP_404_NOT_FOUND,
    )




# register routers
app.include_router(router=api_router, prefix="/api")
app.include_router(router=web_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app", host="0.0.0.0", port=9000, log_level="info", reload=True
    )
