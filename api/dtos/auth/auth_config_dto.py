from dataclasses import dataclass

from .github_oauth_config_dto import GitHubOAuthConfigDTO


@dataclass(slots=True)
class AuthConfigDTO:
    github: GitHubOAuthConfigDTO
    session_secret: str
