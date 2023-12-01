from datetime import datetime

from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from src.db import Base, UTCNow


class Secret(Base):
    secret_key: Mapped[str]
    secret_message: Mapped[str]
    passphrase: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=UTCNow(),
    )
    expires_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
