from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String

from src.core.database.base import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    username: Mapped[str] = mapped_column(String, unique=True)
