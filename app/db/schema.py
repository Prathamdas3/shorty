from sqlmodel import SQLModel, Field
import sqlalchemy as sa
from datetime import datetime
from uuid import UUID, uuid4


class TimestampMixin:
    created_at: datetime | None = Field(
        default=None,
        sa_type=sa.DateTime(timezone=True),
        sa_column_kwargs={"server_default": sa.func.now()},
        nullable=False,
    )

    updated_at: datetime | None = Field(
        default=None,
        sa_type=sa.DateTime(timezone=True),
        sa_column_kwargs={"onupdate": sa.func.now(), "server_default": sa.func.now()},
    )


class Links(TimestampMixin, SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, nullable=False)
    original_url: str = Field(sa_type=sa.String(), nullable=False)
    sort_id: str = Field(sa_type=sa.String(), index=True, nullable=False, unique=True)
    clicks: int = Field(default=0, nullable=False)
    last_accessed_at: datetime | None = Field(
        default=None, sa_type=sa.DateTime(timezone=True), nullable=True
    )
