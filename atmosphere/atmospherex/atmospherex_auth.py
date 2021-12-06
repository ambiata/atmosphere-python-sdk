import datetime
import logging
from typing import Optional

import jwt
import pytz
from pydantic import SecretStr
from pydantic.dataclasses import dataclass
from requests.auth import AuthBase

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AuthSettings:
    jwt_issuer: str
    jwt_subject: str
    jwt_secret: SecretStr
    jwt_expiry_seconds: int = 120
    jwt_sign_algorithm: str = "HS256"
    jwt_audience: str = "atmosphere"


def create_internal_jwt_token(settings: AuthSettings) -> str:
    issued_at = datetime.datetime.now(tz=pytz.utc)
    expires_at = issued_at + datetime.timedelta(seconds=settings.jwt_expiry_seconds)
    internal_jwt = {
        "iss": settings.jwt_issuer,
        "aud": settings.jwt_audience,
        "sub": settings.jwt_subject,
        "iat": issued_at,
        "exp": expires_at,
    }
    str_token = jwt.encode(
        internal_jwt,
        key=settings.jwt_secret.get_secret_value(),
        algorithm=settings.jwt_sign_algorithm,
    )
    return str_token


class BearerTokenAuth(AuthBase):
    """
    requests.AuthBase handling adding the jwt token in the expected
    header of the request.
    If no auth settings are provided, this is a pass through,
    but it will log a warning that the client is sending
    request without authorization headers.
    """

    def __init__(self, settings: Optional[AuthSettings]):
        self.settings = settings

    def __call__(self, r):
        if self.settings:
            token = create_internal_jwt_token(self.settings)
            r.headers.update({"Authorization": f"Bearer {token}"})
        else:
            logger.warning("Calling the atmosphere api without authorization header")
        return r
