from fastapi import APIRouter, Depends, Request, Response, status

from api.constants import (
    GITHUB_OAUTH_HANDSHAKE_COOKIE_NAME,
    GITHUB_OAUTH_HANDSHAKE_TTL_SECONDS,
    SESSION_COOKIE_NAME,
)
from api.controllers.auth import GitHubOAuthController
from api.dependencies.auth import github_oauth_controller
from api.errors.auth import (
    GitHubOAuthCookieNotFoundError,
    UnauthorizedError,
)
from api.errors.defaults import BaseError
from api.errors.general import InternalServerError
from api.schemas.auth import (
    AuthGitHubCompleteRequestBodySchema,
    AuthGitHubStartResponseBodySchema,
)
from api.utilities.datetime import to_iso_string
from api.utilities.logging import get_logger

router = APIRouter(prefix="/api/auth", tags=["auth", "github"])


@router.post("/github/complete")
async def auth_github_complete(
    body: AuthGitHubCompleteRequestBodySchema,
    request: Request,
    response: Response,
    _github_oauth_controller: GitHubOAuthController = Depends(github_oauth_controller),
) -> None:
    logger = get_logger()
    handshake_id = request.cookies.get(GITHUB_OAUTH_HANDSHAKE_COOKIE_NAME)

    if not handshake_id:
        logger.error("missing github oauth handshake cookie")

        raise GitHubOAuthCookieNotFoundError().to_http_exception(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        session, user_added = await _github_oauth_controller.complete(
            code=body.code, handshake_id=handshake_id, state=body.state
        )
        response.status_code = status.HTTP_201_CREATED if user_added else status.HTTP_200_OK

        # delete the handshake cookie
        response.delete_cookie(GITHUB_OAUTH_HANDSHAKE_COOKIE_NAME)

        # add the session cookie
        response.set_cookie(
            key=SESSION_COOKIE_NAME,
            value=str(session.id),
            httponly=True,
            secure=True,
            samesite="lax",
            expires=to_iso_string(session.expires_at),
        )

        return None
    except UnauthorizedError:
        raise UnauthorizedError().to_http_exception(status_code=status.HTTP_401_UNAUTHORIZED)
    except BaseError as e:
        raise e.to_http_exception(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        logger.error(e)

        raise InternalServerError().to_http_exception(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/github/start", response_model=AuthGitHubStartResponseBodySchema, status_code=status.HTTP_201_CREATED)
async def auth_github_start(
    response: Response,
    _github_oauth_controller: GitHubOAuthController = Depends(github_oauth_controller),
) -> AuthGitHubStartResponseBodySchema:
    logger = get_logger()

    try:
        [handshake, authorize_url] = await _github_oauth_controller.start()
    except BaseError as e:
        raise e.to_http_exception(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        logger.error(e)

        raise InternalServerError().to_http_exception(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # save the auth transaction id to the cookie
    response.set_cookie(
        key=GITHUB_OAUTH_HANDSHAKE_COOKIE_NAME,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=GITHUB_OAUTH_HANDSHAKE_TTL_SECONDS,
        path="/",
        value=handshake.id,
    )

    return AuthGitHubStartResponseBodySchema(
        authorize_url=authorize_url,
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def auth_logout(response: Response) -> Response:
    # delete cookies
    response.delete_cookie(GITHUB_OAUTH_HANDSHAKE_COOKIE_NAME, path="/")
    response.delete_cookie(SESSION_COOKIE_NAME)

    return response
