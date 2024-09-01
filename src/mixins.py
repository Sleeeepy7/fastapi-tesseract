from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import event, func, DateTime
from datetime import datetime


class PrimaryKeyMixin:
    id: Mapped[int] = mapped_column(primary_key=True)


class TimeStampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        default=datetime.utcnow,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        default=datetime.utcnow,
    )

    @staticmethod
    def _updated_at(mapper, connection, target):
        target.updated_at = datetime.utcnow()

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, "before_update", cls._updated_at)
