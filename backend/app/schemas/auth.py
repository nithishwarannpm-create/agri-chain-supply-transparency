from typing import Literal

from pydantic import BaseModel, EmailStr, Field


UserRole = Literal[
    "farmer",
    "transporter",
    "distributor",
    "retailer",
    "admin",
]


class UserRegister(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: UserRole


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"