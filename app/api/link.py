from urllib.parse import urlparse
from fastapi import APIRouter, status
from app.models.response import Response, Status

# from app.core.rate_limit import rate_limit
from app.models.input import OriginalUrlInput
from app.services.link import LinkService
from app.db.init import SessionDep

router = APIRouter(prefix="/api")


def normalize_url(url: str) -> str:
    """Normalize URL to lowercase scheme and netloc"""
    parsed = urlparse(url)
    normalized = parsed._replace(
        scheme=parsed.scheme.lower(), netloc=parsed.netloc.lower().rstrip("/")
    )
    return normalized.geturl()


# @rate_limit(max_calls=15, period=30)


@router.post("/link", status_code=status.HTTP_200_OK, response_model=Response)
def generate_new_link(
    # request: Request,
    url: OriginalUrlInput,
    session: SessionDep,
):
    """Generate a new short link for the given URL"""

    # Normalize and create short link
    normalized_url = normalize_url(str(url.link))
    link_service = LinkService(session=session)

    new_link = link_service.generate_new_link(original_link=normalized_url)

    return {
        "status": Status.success,
        "data": new_link,
        "message": "Successfully generated the link",
    }
