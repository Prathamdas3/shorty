from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from app.core.config import config

robots_route = APIRouter()


@robots_route.get("/robots.txt", response_class=PlainTextResponse)
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
