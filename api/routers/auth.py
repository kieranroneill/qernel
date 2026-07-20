from uuid import uuid4

from fastapi import APIRouter, Depends
from redis.asyncio import Redis

from api.dependencies import session_store, system_config
from api.dtos.auth import AuthTransactionDTO
from api.dtos.system import SystemConfigDTO
from api.errors.general import InternalServerError
from api.repositories.auth import AuthTransactionRepository
from api.schemas.auth import AuthGitHubStartRequest, AuthGitHubStartResponse
from api.services.auth import GitHubOAuthService
from api.utilities.datetime import now
from api.utilities.logging import get_logger

router = APIRouter(prefix="/api/auth", tags=["auth", "github"])


@router.post("/github/start", response_model=AuthGitHubStartResponse)
async def auth_github_start(
    request: AuthGitHubStartRequest,
    _session_store: Redis = Depends(session_store),
    _system_config: SystemConfigDTO = Depends(system_config),
) -> AuthGitHubStartResponse:
    logger = get_logger()

    try:
        auth_transaction = AuthTransactionDTO(
            created_at=now(),
            code_verifier=AuthTransactionDTO.generate_code_verifier(),
            id=str(uuid4()),
            next_path=request.next_path or "/app",
            state=AuthTransactionDTO.generate_state(),
        )
        authorize_url = GitHubOAuthService(auth_config=_system_config.auth).generate_authorize_url(
            code_verifier=auth_transaction.code_verifier,
            state=auth_transaction.state,
        )

        # save the auth transaction to the database
        await AuthTransactionRepository(logger=logger, session_store=_session_store).add(auth_transaction)
    except Exception as e:
        logger.error(e)

        raise InternalServerError().to_http_exception(status_code=500)

    return AuthGitHubStartResponse(
        authorize_url=authorize_url,
    )
