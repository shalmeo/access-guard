from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Cookie, Depends
from starlette import status
from starlette.exceptions import HTTPException

from src.application.ioc import InteractorFactory
from src.application.user.dto import UpdateUserDTO
from src.domain.exceptions import AuthenticationError
from src.presentation.web_api.auth import HttpAuthenticator
from src.presentation.web_api.user_update.requests import UpdateMeRequest

user_update_router = APIRouter()


@user_update_router.put("/me")
def user_update(
    data: UpdateMeRequest,
    authenticator: Annotated[HttpAuthenticator, Depends()],
    ioc: Annotated[InteractorFactory, Depends()],
    session_id: str = Cookie(...),
):
    try:
        user_id = authenticator.validate_session(UUID(session_id))
    except AuthenticationError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    with ioc.update_user() as update_user:
        update_user(UpdateUserDTO(user_id=user_id, name=data.name, expired_in=None))

    return "ok"
