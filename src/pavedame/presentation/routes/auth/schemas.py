from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class SignUpRequestSchema(BaseModel):
    username: Annotated[
        str,
        Field(
            min_length=1,
            max_length=64,
            title="Username",
            description="The username to use",
        ),
    ]
    password: Annotated[
        str,
        Field(
            min_length=8,
            max_length=64,
            title="Password",
            description="The password to use",
        ),
    ]
    email: Annotated[
        EmailStr,
        Field(
            title="Email",
            description="The e-mail address of the user",
            examples=["denispometko8@gmail.com"],
        ),
    ]


class SignUpResponseSchema(BaseModel):
    id: Annotated[
        UUID,
        Field(
            title="UserID",
            description="The user ID, stored as UUID",
        ),
    ]


class LoginRequestSchema(BaseModel):
    password: Annotated[
        str,
        Field(
            min_length=8,
            max_length=64,
            title="Password",
            description="The password to use",
        ),
    ]
    email: Annotated[
        EmailStr,
        Field(
            title="Email",
            description="The e-mail address of the user",
            examples=["denispometko8@gmail.com"],
        ),
    ]
