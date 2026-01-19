from urllib.parse import urlparse
from fastapi import APIRouter, status, Request
from app.models.response import Response, Status
from app.models.input import OriginalUrlInput
from app.services.link import LinkService
from app.db.init import SessionDep
from app.services.qr import QrGeneratorService
import base64
from io import BytesIO
from app.core.rate_limit import rate_limit

link_router = APIRouter()


def normalize_url(url: str) -> str:
    """
    Normalize a URL by converting scheme and netloc to lowercase and removing trailing slashes.

    Args:
        url (str): The URL to normalize.

    Returns:
        str: The normalized URL.
    """
    parsed = urlparse(url)
    normalized = parsed._replace(
        scheme=parsed.scheme.lower(), netloc=parsed.netloc.lower().rstrip("/")
    )
    return normalized.geturl()


@link_router.post("/link", status_code=status.HTTP_200_OK, response_model=Response)
@rate_limit(times=5, seconds=60)
def generate_new_link(
    request: Request,
    url: OriginalUrlInput,
    session: SessionDep,
) :
    """
    Generate a new short link for the provided original URL.

    Validates the input URL, normalizes it, and creates a unique short link
    stored in the database.

    Args:
        url (str): The original URL as a query parameter.
        session (SessionDep): Database session dependency.

    Returns:
        Response: JSON response with success status and the short link data.

    Raises:
        ValidationError: If the URL is invalid.
        DbException: If database operations fail.
    """
    # Normalize and create short link
    normalized_url = normalize_url(str(url.link))
    link_service = LinkService(session=session)
    qr_service = QrGeneratorService()
    new_link = link_service.generate_new_link(original_link=normalized_url)

    # Generate QR code
    qr_img = qr_service.generate_qr_image(data=new_link)

    # Convert image to base64
    buffer = BytesIO()
    qr_img.save(buffer, "PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return Response(
        status=Status.success,
        data={"link": new_link, "qr": qr_base64},
        message="Successfully generated the link",
    )
