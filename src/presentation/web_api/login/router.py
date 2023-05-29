from typing import Annotated

from fastapi import APIRouter, Depends
from jinja2 import PackageLoader
from starlette import status
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response
from starlette.templating import Jinja2Templates

from src.application.auth.dto import LoginResultDTO
from src.application.common.exceptions import NotFound
from src.application.ioc import InteractorFactory
from src.domain.exceptions import AccessExpiredError, AuthenticationError
from src.presentation.web_api.auth import HttpAuthenticator

index_router = APIRouter()

jinja_loader = PackageLoader("src.presentation.web_api.login")
templates = Jinja2Templates(directory="templates", loader=jinja_loader)


@index_router.get("/sign-in")
def index(
    request: Request,
):
    return templates.TemplateResponse("login.html", {"request": request})


@index_router.post("/login")
def login(
    login_result: LoginResultDTO,
    ioc: Annotated[InteractorFactory, Depends()],
    authenticator: Annotated[HttpAuthenticator, Depends()],
    response: Response,
) -> str:
    with ioc.authenticate() as authenticate:
        try:
            user_id = authenticate(login_result)
        except (AuthenticationError, AccessExpiredError):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        except NotFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    session_id = authenticator.create_session(user_id)

    response.set_cookie(key="session_id", value=str(session_id))

    return "ok"
