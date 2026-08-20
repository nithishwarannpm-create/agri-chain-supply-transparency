import uuid

from fastapi import APIRouter, HTTPException

from app.schemas.auth import (
    UserLogin,
    UserRegister,
    TokenResponse,
)
from app.services.auth_service import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.services.database import users_collection


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(user: UserRegister):

    existing_user = users_collection.find_one(
        {"email": user.email}
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail={
                "success": False,
                "error": {
                    "code": "EMAIL_ALREADY_EXISTS",
                    "message": "Email is already registered"
                }
            }
        )

    user_id = f"USER-{uuid.uuid4().hex[:8].upper()}"

    user_document = {
        "user_id": user_id,
        "name": user.name,
        "email": user.email,
        "password_hash": hash_password(user.password),
        "role": user.role,
    }

    users_collection.insert_one(user_document)

    return {
        "success": True,
        "user": {
            "user_id": user_id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
        }
    }


@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin):

    existing_user = users_collection.find_one(
        {"email": user.email}
    )

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail={
                "success": False,
                "error": {
                    "code": "INVALID_CREDENTIALS",
                    "message": "Invalid email or password"
                }
            }
        )

    if not verify_password(
        user.password,
        existing_user["password_hash"]
    ):
        raise HTTPException(
            status_code=401,
            detail={
                "success": False,
                "error": {
                    "code": "INVALID_CREDENTIALS",
                    "message": "Invalid email or password"
                }
            }
        )

    token = create_access_token(
        existing_user["user_id"],
        existing_user["role"]
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }