from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from starlette import status

from pavedame.application.auth.login import LoginData, LoginHandler
from pavedame.application.auth.logout import LogoutHandler
from pavedame.application.auth.signup import SignUpData, SignUpHandler
from pavedame.presentation.routes.auth.schemas import LoginRequestSchema, SignUpRequestSchema, SignUpResponseSchema

auth_router: APIRouter = APIRouter(
    prefix="/auth",
    tags=["auth"],
    route_class=DishkaRoute,
)


@auth_router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    summary="Sign up user",
    description="...",
    responses={}
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


@auth_router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    summary="Login user",
    description="...",
    responses={}
)
async def login(
    request: LoginRequestSchema,
    interactor: FromDishka[LoginHandler],
) -> None:
    data = LoginData(
        email=request.email,
        password=request.password,
    )

    await interactor(data=data)

@auth_router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Logout user",
    description="...",
    responses={}
)
async def logout(
    interactor: FromDishka[LogoutHandler],
) -> None:
    await interactor()
