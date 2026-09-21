from fastapi import APIRouter
from starlette import status

from pavedame.application.auth.login import LoginData
from pavedame.application.auth.signup import SignUpData
from pavedame.presentation.routes.auth.schemas import LoginRequestSchema, SignUpRequestSchema, SignUpResponseSchema

auth_router: APIRouter = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@auth_router.post(
    "/signup",
    response_class=status.HTTP_201_CREATED,
    summary="Sign up user",
    description="...",
    responses={}
)
async def sign_up(
        request: SignUpRequestSchema,
        interactor,
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
    response_class=status.HTTP_200_OK,
    summary="Login user",
    description="...",
    responses={}
)
async def login(
        request: LoginRequestSchema,
        interactor,
) -> None:
    data = LoginData(
        email=request.email,
        password=request.password,
    )

    await interactor(data=data)

@auth_router.post(
    "/logout",
    response_class=status.HTTP_204_NO_CONTENT,
    summary="Logout user",
    description="...",
    responses={}
)
async def logout(
        interactor,
) -> None:
    await interactor()
