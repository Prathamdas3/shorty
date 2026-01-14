from urllib.parse import urlparse
from fastapi import APIRouter, status
from fastapi.responses import RedirectResponse
from app.models.response import Response, Status

# from app.core.rate_limit import rate_limit
from app.models.input import OriginalUrlInput, SortIDInput
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


@router.get("/link", status_code=status.HTTP_200_OK, response_model=Response)
def generate_new_link(
    # request: Request,
    url: str,
    session: SessionDep,
):
    """Generate a new short link for the given URL"""
    # Validate input
    link_input = OriginalUrlInput(link=url)

    # Normalize and create short link
    normalized_url = normalize_url(str(link_input.link))
    link_service = LinkService(session=session)

    new_link = link_service.generate_new_link(original_link=normalized_url)

    return {
        "status": Status.success,
        "data": new_link,
        "message": "Successfully generated the link",
    }


@router.get("/{short_id}", response_class=RedirectResponse)
def redirect_to_original_link(short_id: str, session: SessionDep):
    """Redirect to the original URL using the short ID"""
    # Validate input
    id_input = SortIDInput(sort_id=short_id)

    # Get original link and redirect
    link_service = LinkService(session=session)
    original_url = link_service.get_original_link(sort_id=id_input.sort_id)

    return RedirectResponse(
        url=original_url, status_code=status.HTTP_301_MOVED_PERMANENTLY
    )
