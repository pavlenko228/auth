#создание, удаление, чтение пользователей
import httpx
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from api.api_v1.utils import create_access_token, create_refresh_token, hash_password
from core.config import settings
from core.models import db_helper
from core.models.auth import Auth
from core.schemas.user import CreateUser
from core.schemas.jwt import TokenInfo

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix=settings.api.v1.users,
    tags=["users"],
    dependencies=[Depends(http_bearer)],
)

@router.post("/create_user", response_model=TokenInfo)
async def create_user(
    user: CreateUser,
    db: AsyncSession = Depends(db_helper.session_getter)
):
    user_uuid = str(uuid.uuid4())
    email = user.email
    hashed_password = hash_password(user.password)

    new_user = Auth(uuid=user_uuid, email=email, hashed_password=hashed_password)

    try:
        db.add(new_user)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")

    access_token = create_access_token(data={"uuid": user_uuid, "scope": "create_user"})
    refresh_token = create_refresh_token(data={"uuid": user_uuid})

    user_service_url = "http://user_service_host/create_user"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(user_service_url, json={"uuid": user_uuid}, headers=headers)
            response.raise_for_status()  # Проверка на ошибки HTTP
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error calling user service: {str(e)}")

    return TokenInfo(access_token=access_token, refresh_token=refresh_token)
