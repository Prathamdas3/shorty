from sqlmodel import select, Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from datetime import datetime
from app.db.schema import Links
from app.core.logger import get_logger
from app.core.exception import DbException, AppException
from app.core.config import config
import string
import secrets

logger = get_logger(__name__)
ALPHABET = string.ascii_letters + string.digits



class LinkService:
    """
    Service class for managing URL shortening operations.

    Handles creation of short links, retrieval of original URLs,
    and database interactions for link management.
    """

    def __init__(self, session: Session):
        """
        Initialize the LinkService with a database session.

        Args:
            session (Session): SQLAlchemy database session.
        """
        self._db = session

    def _commit(self) -> None:
        """
        Commit database changes with error handling.

        Attempts to commit the current transaction. Rolls back on failure
        and raises a DbException.

        Raises:
            DbException: If the commit operation fails.
        """
        try:
            self._db.commit()
        except (IntegrityError, SQLAlchemyError) as e:
            self._db.rollback()
            logger.error("Database operation failed", exc_info=True)
            raise DbException(f"Database operation failed {str(e)}")

    def _create_unique_id(self, length: int = 7) -> str:
        """
        Generate a unique random ID of specified length.

        Args:
            length (int): Length of the ID to generate. Defaults to 7.

        Returns:
            str: Randomly generated unique ID.
        """
        return "".join(secrets.choice(ALPHABET) for _ in range(length))

    def generate_new_link(self, original_link: str) -> str:
        """
        Create a new short link for the given original URL.

        Generates a unique short ID, stores the link in the database,
        and returns the short link URL.

        Args:
            original_link (str): The original URL to shorten.

        Returns:
            Short link URL as str.

        Raises:
            DbException: If database operations fail.
            AppException: If link generation fails.
        """
        try:
            sort_id = self._create_unique_id()
            new_link = Links(original_url=original_link, sort_id=sort_id)
            self._db.add(new_link)
            self._commit()
            self._db.refresh(new_link)

            logger.debug(f"New link created successfully with id {new_link.id}")
            return f"{config.frontend_url}/{sort_id}"

        except Exception as e:
            logger.error(f"Failed to generate new link {str(e)}")
            raise AppException("Failed to generate a new link")

    def get_original_link(self, sort_id: str) -> str:
        """
        Retrieve the original URL for a given short ID.

        Increments the click count and updates the last accessed timestamp.
        Returns the 404 page URL if the short ID is not found.

        Args:
            sort_id (str): The short ID to look up.

        Returns:
            str: The original URL or 404 page URL if not found.

        Raises:
            DbException: If database operations fail.
            AppException: If retrieval fails.
        """
        try:
            statement = select(Links).where(Links.sort_id == sort_id)
            old_link = self._db.exec(statement=statement).one_or_none()
            if not old_link:
                return f"{config.frontend_url}/404"

            old_link.clicks = old_link.clicks + 1
            old_link.last_accessed_at = datetime.now()

            self._db.add(old_link)
            self._commit()

            logger.debug("Updated and fetched the old link")
            return old_link.original_url
        except Exception:
            logger.error("Failed to find the original link")
            raise AppException("Failed to find the original link")
