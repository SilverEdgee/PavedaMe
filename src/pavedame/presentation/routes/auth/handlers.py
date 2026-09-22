from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query, Response
from starlette import status

from pavedame.application.auth.email_verification_model import RawEmailVerificationToken
from pavedame.application.auth.login import LoginData, LoginHandler
from pavedame.application.auth.logout import LogoutHandler
from pavedame.application.auth.signup import SignUpData, SignUpHandler
from pavedame.application.auth.verify_email import VerifyEmailHandler
from pavedame.presentation.routes.auth.schemas import LoginRequestSchema, SignUpRequestSchema, SignUpResponseSchema

auth_router: APIRouter = APIRouter(
    prefix="/auth",
    tags=["auth"],
    route_class=DishkaRoute,
)


@auth_router.post(
    "/signup", status_code=status.HTTP_201_CREATED, summary="Sign up user", description="...", responses={}
)
async def sign_up(
    request: SignUpRequestSchema,
    interactor: FromDishka[SignUpHandler],
) -> SignUpResponseSchema:
    data = SignUpData(
        username=request.username,
        email=request.email,
        password=request.password,
    )

    view = await interactor(data=data)

    return SignUpResponseSchema(id=view.id)


@auth_router.post("/login", status_code=status.HTTP_200_OK, summary="Login user", description="...", responses={})
async def login(
    request: LoginRequestSchema,
    interactor: FromDishka[LoginHandler],
    response: FromDishka[Response],
) -> Response:
    data = LoginData(
        email=request.email,
        password=request.password,
    )

    await interactor(data=data)
    return response


@auth_router.get(
    "/verify-email",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Verify email",
    description="Verify an email address and authenticate the user.",
    responses={},
)
async def verify_email(
    token: Annotated[str, Query(min_length=32)],
    interactor: FromDishka[VerifyEmailHandler],
    response: FromDishka[Response],
) -> Response:
    await interactor(RawEmailVerificationToken(token))
    response.status_code = status.HTTP_204_NO_CONTENT
    return response


@auth_router.post(
    "/logout", status_code=status.HTTP_204_NO_CONTENT, summary="Logout user", description="...", responses={}
)
async def logout(
    interactor: FromDishka[LogoutHandler],
    response: FromDishka[Response],
) -> Response:
    await interactor()
    response.status_code = status.HTTP_204_NO_CONTENT
    return response
