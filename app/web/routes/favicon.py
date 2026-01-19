from fastapi import APIRouter
from fastapi.responses import FileResponse

icon_route = APIRouter()


@icon_route.get("/favicon.ico", include_in_schema=False)
def favicon():
    return FileResponse("static/icons/favicon.ico")
