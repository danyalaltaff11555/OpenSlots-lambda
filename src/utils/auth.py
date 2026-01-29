from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional
import jwt
import config


@dataclass
class TokenPayload:
    org_id: str
    user_id: str
    role: str
    exp: datetime


def create_token(org_id: str, user_id: str, role: str) -> str:
    exp = datetime.utcnow() + timedelta(hours=config.TOKEN_EXPIRY_HOURS)
    payload = {"org_id": org_id, "user_id": user_id, "role": role, "exp": exp}
    return jwt.encode(payload, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)


def validate_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(
            token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM]
        )
        return TokenPayload(
            org_id=payload["org_id"],
            user_id=payload["user_id"],
            role=payload["role"],
            exp=datetime.fromtimestamp(payload["exp"]),
        )
    except jwt.ExpiredSignatureError:
        raise Exception("Token expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")


def extract_token(auth_header: str) -> str:
    if auth_header.startswith("Bearer "):
        return auth_header[7:]
    return auth_header
