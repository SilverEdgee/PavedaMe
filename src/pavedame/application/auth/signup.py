from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True, slots=True)
class SignUpData:
    username: str
    password: str
    email: str
