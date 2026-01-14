from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app.core.config import config
from app.core.logger import get_logger
from app.api.link import router
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

# register the exceptions
app.add_exception_handler(DbException, db_exception_handler)
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(LinkNotFound, link_not_found_handler)


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.critical(
        f"Unhandled exception: {str(exc)} - Path: {request.url.path}", exc_info=True
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An internal server error occurred.",
            "error_type": "internal_server_error",
        },
    )


# register routers
app.include_router(router=router)

# root level routes
app.get("/", status_code=status.HTTP_200_OK)


def handle_home_page():
    return {"Hello": "heelo"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app", host="0.0.0.0", port=20000, log_level="info", reload=True
    )
