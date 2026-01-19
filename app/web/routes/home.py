from fastapi import Request, status, APIRouter
from app.core.template import templates
from app.core.config import config
from datetime import datetime

home_route = APIRouter()


@home_route.get("/", status_code=status.HTTP_200_OK)
def handle_home_page(request: Request):
    """
    Render the home page with the URL shortening form.

    Args:
        request (Request): The incoming HTTP request.

    Returns:
        TemplateResponse: Rendered home.html template with current year.
    """
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "year": datetime.now().year,
            "config": config,
        },
        status_code=status.HTTP_200_OK,
    )
