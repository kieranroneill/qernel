from dataclasses import dataclass


@dataclass(slots=True)
class GitHubOAuthConfigDTO:
    client_id: str
    client_secret: str
    redirect_uri: str
    scope: str
