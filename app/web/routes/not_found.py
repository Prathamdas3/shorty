from fastapi import APIRouter, status, Request
from app.core.template import templates
from datetime import datetime
from app.core.config import config

not_found_route = APIRouter()


@not_found_route.get("/404", status_code=status.HTTP_404_NOT_FOUND)
def handle_Not_found_page(request: Request):
    """
    Render the 404 error page for invalid short URLs.

    Args:
        request (Request): The incoming HTTP request.

    Returns:
        TemplateResponse: Rendered 404.html template with current year.
    """
    return templates.TemplateResponse(
        "404.html",
        {
            "request": request,
            "year": datetime.now().year,
            "config": config,
        },
        status_code=status.HTTP_404_NOT_FOUND,
    )
