from fastapi import APIRouter

from .jwt_auth import router as jwt_auth_router
from .users import router as users_router

from core.config import settings

router = APIRouter(
    prefix=settings.api.v1.prefix,
)
router.include_router(jwt_auth_router)
router.include_router(users_router)