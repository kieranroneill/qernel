import base64
import hashlib
import secrets
from urllib.parse import urlencode

import httpx

from api.dtos.auth import GitHubOAuthConfigDTO
from api.schemas.github import GitHubEmailResponseSchema, GitHubProfileResponseSchema
from api.utilities.logging import get_logger


class GitHubOAuthService:
    """
    Encapsulates GitHub OAuth and authenticated-user lookups.
    """

    def __init__(self, github_oauth_config: GitHubOAuthConfigDTO) -> None:
        self._authorize_base_url = "https://github.com/login/oauth/authorize"
        self._github_oauth_config = github_oauth_config
        self._logger = get_logger()

    ##
    # private methods
    ##
    @classmethod
    def _generate_code_challenge_from_code_verifier(cls, verifier: str) -> str:
        """
        Creates the PKCE S256 code challenge for the authorization request.

        Args:
            verifier (str): The PKCE code verifier.

        Returns:
            str: The derived PKCE S256 code challenge.
        """

        digest = hashlib.sha256(verifier.encode("utf-8")).digest()

        return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("utf-8")

    ##
    # public static methods
    ##
    @classmethod
    def generate_code_verifier(cls) -> str:
        """
        Generates a high-entropy PKCE code verifier.

        Returns:
            str: A URL-safe random PKCE code verifier.
        """

        return secrets.token_urlsafe(64)

    @classmethod
    def generate_state(cls) -> str:
        """Generate an anti-forgery OAuth state token.

        Returns:
            str: A URL-safe random OAuth state value.
        """

        return secrets.token_urlsafe(32)

    ##
    # public methods
    ##
    async def fetch_emails(self, access_token: str) -> list[GitHubEmailResponseSchema]:
        """
        Fetches the authenticated user's email addresses from GitHub.

        Endpoint: GET https://api.github.com/user/emails
        Docs: https://docs.github.com/en/rest/users/emails#list-email-addresses-for-the-authenticated-user

        Args:
            access_token (str): A GitHub access token for the authenticated user.

        Returns:
            list[GitHubEmailResponseSchema]: Parsed GitHub email records.
        """

        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.github.com/user/emails",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/vnd.github+json",
                    "X-GitHub-Api-Version": "2026-03-10",
                },
            )
            response.raise_for_status()

            data = response.json()

            return [GitHubEmailResponseSchema(**e) for e in data]

    async def fetch_profile(self, access_token: str) -> GitHubProfileResponseSchema:
        """
        Fetches the authenticated GitHub user's profile.

        Endpoint: GET https://api.github.com/user
        Docs: https://docs.github.com/en/rest/users/users#get-the-authenticated-user

        Args:
            access_token (str): A GitHub access token for the authenticated user.

        Returns:
            GitHubProfileResponseSchema: Parsed GitHub user profile data.
        """

        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/vnd.github+json",
                    "X-GitHub-Api-Version": "2026-03-10",
                },
            )
            response.raise_for_status()

            data = response.json()

            return GitHubProfileResponseSchema(**data)

    async def generate_access_token(self, code: str, code_verifier: str) -> str:
        """
        Exchanges an authorization code for an access token.

        Endpoint: POST https://github.com/login/oauth/access_token
        Docs: https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps

        Args:
            code (str): The OAuth authorization code returned by GitHub.
            code_verifier (str): The PKCE code verifier originally used in the authorize request.

        Returns:
            str: The GitHub access token.
        """

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://github.com/login/oauth/access_token",
                headers={"Accept": "application/json"},
                data={
                    "client_id": self._github_oauth_config.client_id,
                    "client_secret": self._github_oauth_config.client_secret,
                    "code": code,
                    "code_verifier": code_verifier,
                    "redirect_uri": str(self._github_oauth_config.redirect_uri),
                },
            )
            response.raise_for_status()
            payload = response.json()

            return payload["access_token"]

    def generate_authorize_url(self, code_verifier: str, state: str) -> str:
        """
        Builds the GitHub authorization URL for the browser redirect.

        Endpoint: GET https://github.com/login/oauth/authorize
        Docs: https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps

        Args:
            code_verifier (str): The PKCE code verifier used to derive the challenge.
            state (str): The OAuth state token used to prevent CSRF.

        Returns:
            str: A fully encoded GitHub authorization URL.
        """

        query = {
            "allow_signup": "false",
            "client_id": self._github_oauth_config.client_id,
            "code_challenge": GitHubOAuthService._generate_code_challenge_from_code_verifier(code_verifier),
            "code_challenge_method": "S256",
            "redirect_uri": self._github_oauth_config.redirect_uri,
            "scope": self._github_oauth_config.scope,
            "state": state,
        }

        return f"https://github.com/login/oauth/authorize?{urlencode(query)}"

    def resolve_primary_email(self, emails: list[GitHubEmailResponseSchema]) -> str:
        """
        Selects the best available email from the GitHub API response.

        Args:
            emails (list[GitHubEmailResponseSchema]): Email records returned by GitHub.

        Returns:
            str: The selected email address.

        Raises:
            ValueError: If no usable emails are returned from GitHub.
        """

        primary_verified = next(
            (e.email for e in emails if e.email and e.verified),
            None,
        )
        verified = next((e.email for e in emails if e.verified), None)
        fallback = next((e.email for e in emails if e.email), None)

        if primary_verified:
            return primary_verified
        if verified:
            return verified
        if fallback:
            return fallback

        raise ValueError("no usable emails returned from github")
