from datetime import datetime
from fastapi import FastAPI, Request, status
from fastapi.responses import (
    RedirectResponse,
    PlainTextResponse,
    Response,
    FileResponse,
)
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select

from app.core.config import config
from app.core.logger import get_logger
from app.api.link import router
from app.services.link import LinkService
from app.models.input import SortIDInput
from app.db.init import SessionDep, db
from app.db.schema import Links
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


@app.get("/robots.txt", response_class=PlainTextResponse)
def robots_txt():
    """
    Serve robots.txt file for search engines and AI crawlers.

    Returns:
        PlainTextResponse: robots.txt content with proper headers.
    """
    robots_content = """# Allow search engines
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

# Allow AI crawlers for training
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: CCBot
Allow: /

User-agent: PerplexityBot
Allow: /

# Block sensitive areas
User-agent: *
Disallow: /api/
Disallow: /docs
Disallow: /admin/
Disallow: /logs/

# Sitemap location
Sitemap: {site_url}/sitemap.xml
""".format(site_url=config.site_url)

    return PlainTextResponse(
        content=robots_content.strip(),
        media_type="text/plain",
        headers={"Cache-Control": "public, max-age=86400"},
    )


@app.get("/sitemap.xml", response_class=Response)
def sitemap_xml():
    """
    Generate dynamic sitemap.xml for search engines.

    Returns:
        Response: XML sitemap with proper headers and caching.
    """
    from sqlmodel import Session

    with Session(db.engine) as session:
        statement = select(Links).order_by(Links.created_at.desc()).limit(50000)
        links = session.exec(statement).all()

    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    xml_content += f"""  <url>
    <loc>{config.site_url}/</loc>
    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>\n"""

    xml_content += f"""  <url>
    <loc>{config.site_url}/404</loc>
    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.1</priority>
  </url>\n"""

    for link in links:
        lastmod_date = link.updated_at if link.updated_at else link.created_at
        xml_content += f"""  <url>
    <loc>{config.frontend_url}/{link.sort_id}</loc>
    <lastmod>{lastmod_date.strftime("%Y-%m-%d") if lastmod_date else datetime.now().strftime("%Y-%m-%d")}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.5</priority>
  </url>\n"""

    xml_content += "</urlset>"

    return Response(
        content=xml_content,
        media_type="application/xml",
        headers={"Cache-Control": "public, max-age=86400"},
    )


# register routers
app.include_router(router=router)


# root level routes
@app.get("/", status_code=status.HTTP_200_OK)
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


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return FileResponse("static/icons/favicon.ico")


@app.get("/404", status_code=status.HTTP_404_NOT_FOUND)
def handle_404_page(request: Request):
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


@app.get("/{short_id}")
def redirect_short_id(short_id: str, session: SessionDep):
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
