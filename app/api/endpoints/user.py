from fastapi import HTTPException, APIRouter

from app.core.user import fastapi_users, auth_backend
from app.schemas.user import UserCreate, UserRead, UserUpdate


router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth']
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth']
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='/users',
    tags=['user']
)


@router.delete(
    '/users/{id}',
    tags=['user'],
    deprecated=True
)
def delete_user(id: str):
    raise HTTPException(
        status_code=422,
        detail='Удаление пользователя запрещено!'
    )
