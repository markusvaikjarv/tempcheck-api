import jwt
from jwt import PyJWKClient
from fastapi import HTTPException, Header
from typing import Annotated
import os

JWKS_URL = os.getenv("JWKS_URL")
if not isinstance(JWKS_URL, str):
    raise ValueError("JWKS_URL is not set")

jwks_client = PyJWKClient(JWKS_URL)

async def get_user_id(authorization: Annotated[str, Header()]) -> str:
    if not isinstance(JWKS_URL, str):
        raise ValueError("JWKS_URL is not set")
    signing_key = jwks_client.get_signing_key_from_jwt(authorization)

    try:
        decoded = jwt.decode(
            authorization,
            signing_key,
            algorithms=["RS256"],
            options={"verify_aud": False, "verify_signature": True},
        )
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    return decoded["sub"]