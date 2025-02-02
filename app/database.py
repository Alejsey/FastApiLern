from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column, sessionmaker
from sqlalchemy import func, create_engine
from app.config import get_db_url
from datetime import datetime
from typing import Annotated

DATABASE_URL = get_db_url()

engine = create_engine(DATABASE_URL)


async_session_maker = sessionmaker(engine)

# настройка аннотаций
int_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
str_null_true = Annotated[str, mapped_column(nullable=True)]


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
