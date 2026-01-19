from fastapi import APIRouter
from app.web.routes import not_found, home, short_id, favicon, robots, sitemap

web_router = APIRouter()

web_router.include_router(router=home.home_route)
web_router.include_router(router=not_found.not_found_route)
web_router.include_router(router=favicon.icon_route)
web_router.include_router(router=robots.robots_route)
web_router.include_router(router=sitemap.sitemap_router)
web_router.include_router(router=short_id.id_route)  # Must be last - catch-all route
