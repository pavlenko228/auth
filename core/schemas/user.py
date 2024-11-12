from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr, ConfigDict


class UserRead(BaseModel):
    email: Annotated[EmailStr, MaxLen(255)]


class CreateUser(UserRead):
    password: Annotated[str, MinLen(10), MaxLen(50)]
    

