from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Cookie, Depends
from jinja2 import PackageLoader
from starlette import status
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from src.application.ioc import InteractorFactory
from src.domain.exceptions import AuthenticationError
from src.presentation.formatter import datetime_format
from src.presentation.web_api.auth import HttpAuthenticator

user_profile_router = APIRouter()

jinja_loader = PackageLoader("src.presentation.web_api.user_profile")
templates = Jinja2Templates(directory="templates", loader=jinja_loader)
templates.env.filters["datetimeformat"] = datetime_format


@user_profile_router.get("/profile")
def profile(
    request: Request,
    authenticator: Annotated[HttpAuthenticator, Depends()],
    ioc: Annotated[InteractorFactory, Depends()],
    session_id: str = Cookie(...),
):
    try:
        user_id = authenticator.validate_session(UUID(session_id))
    except AuthenticationError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    with ioc.get_user_by_id() as get_user_by_id:
        try:
            user = get_user_by_id(data=user_id)
        except AuthenticationError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    return templates.TemplateResponse(
        "profile.html",
        {"request": request, "user": user},
    )
