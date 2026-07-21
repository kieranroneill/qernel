from fastapi import Request

from api.controllers.auth import GitHubOAuthController


async def github_oauth_controller(request: Request) -> GitHubOAuthController:
    return GitHubOAuthController(
        database=request.app.state.database,
        github_oauth_config=request.app.state.auth.github,
        session_store=request.app.state.session_store,
    )
