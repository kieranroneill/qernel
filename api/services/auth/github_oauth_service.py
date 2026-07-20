import base64
import hashlib
from urllib.parse import urlencode

from api.dtos.system import AuthConfigDTO
from api.utilities.logging import get_logger


class GitHubOAuthService:
    def __init__(self, auth_config: AuthConfigDTO) -> None:
        self._auth_config = auth_config
        self._authorize_base_url = "https://github.com/login/oauth/authorize"
        self._logger = get_logger()

    ##
    # private methods
    ##
    @classmethod
    def _generate_code_challenge_from_code_verifier(cls, verifier: str) -> str:
        digest = hashlib.sha256(verifier.encode("utf-8")).digest()

        return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("utf-8")

    ##
    # public methods
    ##
    def generate_authorize_url(self, code_verifier: str, state: str) -> str:
        query = {
            "allow_signup": "false",
            "client_id": self._auth_config.github_client_id,
            "code_challenge": GitHubOAuthService._generate_code_challenge_from_code_verifier(code_verifier),
            "code_challenge_method": "S256",
            "redirect_uri": self._auth_config.github_redirect_uri,
            "scope": self._auth_config.github_scope,
            "state": state,
        }

        return f"{self._authorize_base_url}?{urlencode(query)}"
