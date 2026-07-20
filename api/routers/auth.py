import base64
import json

from fastapi import APIRouter, Depends, Request, Response, status

from api.constants import GITHUB_OAUTH_COOKIE_NAME, GITHUB_OAUTH_HANDSHAKE_TTL_SECONDS
from api.controllers.auth import GitHubOAuthController
from api.dependencies import github_oauth_controller
from api.errors.auth import (
    GitHubOAuthCookieNotFoundError,
    InvalidGitHubOAuthCookieError,
    UnauthorizedError,
)
from api.errors.defaults import BaseError
from api.errors.general import InternalServerError
from api.schemas.auth import (
    AuthGitHubCompleteRequestBodySchema,
    AuthGitHubStartRequestBodySchema,
    AuthGitHubStartResponseBodySchema,
)
from api.utilities.logging import get_logger

router = APIRouter(prefix="/api/auth", tags=["auth", "github"])


@router.post("/github/complete", response_model=AuthGitHubStartResponseBodySchema)
async def auth_github_complete(
    body: AuthGitHubCompleteRequestBodySchema,
    request: Request,
    response: Response,
    _github_oauth_controller: GitHubOAuthController = Depends(github_oauth_controller),
) -> None:
    logger = get_logger()
    cookie = request.cookies.get(GITHUB_OAUTH_COOKIE_NAME)

    if not cookie:
        logger.error("missing github oauth cookie")

        raise GitHubOAuthCookieNotFoundError().to_http_exception(status_code=status.HTTP_403_FORBIDDEN)

    try:
        cookie_payload = json.loads(base64.urlsafe_b64decode(cookie.encode("utf-8")).decode("utf-8"))
    except Exception as e:
        logger.error(e)

        raise InvalidGitHubOAuthCookieError(message="unable to decode github oauth cookie").to_http_exception(
            status_code=status.HTTP_403_FORBIDDEN
        )

    handshake_id = cookie_payload["handshake_id"]

    if not handshake_id:
        error = "no handshake id found in cookie"

        logger.error(error)

        raise InvalidGitHubOAuthCookieError(message=error).to_http_exception(status_code=status.HTTP_403_FORBIDDEN)

    try:
        user, user_added = await _github_oauth_controller.complete(
            code=body.code, handshake_id=handshake_id, state=body.state
        )
        response.status_code = status.HTTP_201_CREATED if user_added else status.HTTP_200_OK

        # TODO: setup cookie session with jwt
    except UnauthorizedError:
        raise UnauthorizedError().to_http_exception(status_code=status.HTTP_401_UNAUTHORIZED)
    except BaseError as e:
        raise e.to_http_exception(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        logger.error(e)

        raise InternalServerError().to_http_exception(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/github/start", response_model=AuthGitHubStartResponseBodySchema, status_code=status.HTTP_201_CREATED)
async def auth_github_start(
    body: AuthGitHubStartRequestBodySchema,
    response: Response,
    _github_oauth_controller: GitHubOAuthController = Depends(github_oauth_controller),
) -> AuthGitHubStartResponseBodySchema:
    logger = get_logger()

    try:
        [handshake, authorize_url] = await _github_oauth_controller.start(next_path=body.next_path)
    except BaseError as e:
        raise e.to_http_exception(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        logger.error(e)

        raise InternalServerError().to_http_exception(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # save the auth transaction id to the cookie
    response.set_cookie(
        key=GITHUB_OAUTH_COOKIE_NAME,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=GITHUB_OAUTH_HANDSHAKE_TTL_SECONDS,
        path="/",
        value=base64.urlsafe_b64encode(
            json.dumps(
                {
                    "handshake_id": handshake.id,
                }
            ).encode("utf-8")
        ).decode("utf-8"),
    )

    return AuthGitHubStartResponseBodySchema(
        authorize_url=authorize_url,
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def auth_logout(response: Response) -> Response:
    # delete cookies
    response.delete_cookie(GITHUB_OAUTH_COOKIE_NAME, path="/")

    return response
