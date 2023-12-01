from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column
from sqlalchemy.sql import expression
from sqlalchemy.types import DateTime

from src.config import settings

engine = create_async_engine(url=str(settings.POSTGRES_DSN), echo=settings.DB_ECHO)

async_session_maker = async_sessionmaker(
    bind=engine, autoflush=False, expire_on_commit=False
)


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(primary_key=True)


class UTCNow(expression.FunctionElement):  # type: ignore
    type = DateTime()
    inherit_cache = True


@compiles(UTCNow, "postgresql")  # type: ignore
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


@compiles(UTCNow, "sqlite")  # type: ignore
def sqlite_utcnow(element, compiler, **kw):
    return "datetime(CURRENT_TIMESTAMP, 'utc')"
