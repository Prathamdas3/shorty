from fastapi import APIRouter
from app.api.routes.link import link_router

api_router = APIRouter()

api_router.include_router(router=link_router)
