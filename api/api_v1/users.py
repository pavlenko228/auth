#создание, удаление, чтение пользователей
from fastapi import APIRouter, Depends, HTTPException, requests
from fastapi.security import HTTPBearer

from sqlalchemy.ext.asyncio import AsyncSession
import uuid


from api.api_v1.utils import create_access_token, create_refresh_token, hash_password
from core.config import settings
from core.models import db_helper
from core.models.auth import Auth
from core.schemas import UserCreate
from core.schemas.jwt import TokenInfo


http_bearer = HTTPBearer(auto_error=False)


router = APIRouter(
    prefix=settings.api.v1.users,
    tags=["users"],
    dependencies=[Depends(http_bearer)],
)


@router.post("/create_user", response_model=TokenInfo)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(db_helper.session_getter)
):
    uuid = str(uuid.uuid4())
    email = user.email
    hashed_password = hash_password(user.password)

    new_user = Auth(uuid=uuid, email=email, hashed_password=hashed_password)

    try:
        db.add(new_user)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error saving user: {str(e)}")

    access_token = create_access_token(data={"uuid": uuid, "scope": "create_user"})
    refresh_token = create_refresh_token(data={"uuid": uuid})

    user_service_url = "http://user_service_host/create_user"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:
        response = requests.post(user_service_url, json={"uuid": uuid}, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Error calling user service")
    return TokenInfo(access_token=access_token, refresh_token=refresh_token)
