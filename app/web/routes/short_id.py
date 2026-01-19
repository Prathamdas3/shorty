from fastapi import APIRouter, status
from fastapi.responses import RedirectResponse
from app.db.init import SessionDep
from app.models.input import SortIDInput
from app.services.link import LinkService

id_route = APIRouter()


@id_route.get("/{short_id}")
def redirect_short_id(short_id: str, session: SessionDep):
    """
    Redirect to the original URL for a given short ID.

    Validates the short ID, retrieves the original URL from the database,
    and performs a permanent redirect.

    Args:
        short_id (str): The short ID to redirect from.
        session: Database session provided by the dependency.

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
