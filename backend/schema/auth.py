# -*- coding: utf-8 -*-
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenVerificationResult(BaseModel):
    is_valid: bool
    is_expired: bool
    uid: int | None
    exp: int | None

class VerifyTokenRequest(BaseModel):
    token: str

class UserInfo(BaseModel):
    uid: int
    username: str
    role: str
    phone: str
