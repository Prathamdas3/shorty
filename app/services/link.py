from sqlmodel import select, Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from datetime import datetime
from typing import TypedDict
from app.db.schema import Links
from app.core.logger import get_logger
from app.core.exception import DbException, AppException
from app.core.config import config
import string
import secrets

logger = get_logger(__name__)
ALPHABET = string.ascii_letters + string.digits


class ReturnLinkDict(TypedDict):
    link: str


class LinkService:
    def __init__(self, session: Session):
        self._db = session

    def _commit(self) -> None:
        try:
            self._db.commit()
        except (IntegrityError, SQLAlchemyError) as e:
            self._db.rollback()
            logger.error("Database operation failed", exc_info=True)
            raise DbException(f"Database operation failed {str(e)}")

    def _create_unique_id(self, length: int = 7) -> str:
        return "".join(secrets.choice(ALPHABET) for _ in range(length))

    def generate_new_link(self, original_link: str) -> ReturnLinkDict:
        """Creating new link form the original link

        Args:
            original_link (str): it takes the original link

        Returns:
            dict: returns dict with a field of link
        """
        try:
            sort_id = self._create_unique_id()
            new_link = Links(original_url=original_link, sort_id=sort_id)
            self._db.add(new_link)
            self._commit()
            self._db.refresh(new_link)

            logger.debug(f"New link created successfully with id {new_link.id}")
            return {"link": f"{config.frontend_url}/{sort_id}"}

        except Exception as e:
            logger.error(f"Failed to generate new link {str(e)}")
            raise AppException("Failed to generate a new link")

    def get_original_link(self, sort_id: str):
        """Recives a sort id and finds the original url based on that id

        Args:
            sort_id (str): sort id associated with the original url

        Raises:
            AppException: Faild to perform the operation to find the original link

        Returns:
            ReturnLinkDict: Returns link as the only field
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
