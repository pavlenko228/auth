#routs аутентификация, выпуск и перевыпуск токенов

from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.security import (
    HTTPBearer,
    # HTTPAuthorizationCredentials,
)
from core.schemas.jwt import TokenInfo

from api_v1.utils import (
    get_current_token_payload,
    create_access_token,
    create_refresh_token,
)
from api_v1.validation import (
    get_current_auth_user_for_refresh,
    get_current_active_auth_user,
    validate_auth_user,
    # REFRESH_TOKEN_TYPE,
    # get_auth_user_from_token_of_type,
    # UserGetterFromToken,
)
from core.schemas.user import CreateUser

from core.config import settings

http_bearer = HTTPBearer(auto_error=False)


router = APIRouter(
    prefix=settings.api.v1.jwt_auth,
    tags=["JWT"],
    dependencies=[Depends(http_bearer)],
)


@router.post("/login/", response_model=TokenInfo)
def auth_user_issue_jwt(
    user: CreateUser = Depends(validate_auth_user),
):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post(
    "/refresh/",
    response_model=TokenInfo,
    response_model_exclude_none=True,
)
def auth_refresh_jwt(
    user: CreateUser = Depends(get_current_auth_user_for_refresh),
):
    access_token = create_access_token(user)
    return TokenInfo(
        access_token=access_token,
    )


# @router.get("/users/me/")
# def auth_user_check_self_info(
#     payload: dict = Depends(get_current_token_payload),
#     user: CreateUser = Depends(get_current_active_auth_user),
# ):
#     iat = payload.get("iat")
#     return {
#         "username": user.username,
#         "email": user.email,
#         "logged_in_at": iat,
#     }