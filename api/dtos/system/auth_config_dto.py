from dataclasses import dataclass


@dataclass(slots=True)
class AuthConfigDTO:
    github_client_id: str
    github_client_secret: str
    github_redirect_uri: str
    github_scope: str
    session_cookie_name: str
    session_secret: str
