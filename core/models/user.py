import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    __tablename__ = 'auth'

    uuid: Mapped[str] = mapped_column(String, unique=True, primary_key=True) #default=str(uuid.uuid4())
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)