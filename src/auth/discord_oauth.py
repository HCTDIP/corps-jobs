"""
Discord OAuth authentication handler for YapHub.
Fixes HTTP 429 rate limiting from Railway US East edge proxy.
"""

import logging
import time
import httpx
from typing import Optional
from src.services.retry_policy import ExponentialBackoffWithJitter

logger = logging.getLogger(__name__)

DISCORD_OAUTH_TOKEN_URL = "https://discord.com/api/oauth2/token"
DISCORD_USERINFO_URL = "https://discord.com/api/users/@me"


class DiscordOAuthHandler:
    """Handles Discord OAuth flow with rate-limit-aware retries."""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        retry_policy: Optional[ExponentialBackoffWithJitter] = None,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.retry_policy = retry_policy or ExponentialBackoffWithJitter(
            max_retries=5,
            base_delay=1.0,
            max_delay=30.0,
            jitter=True,
        )
        self._client = httpx.AsyncClient(timeout=15.0)

    async def exchange_code_for_token(
        self, authorization_code: str
    ) -> dict:
        """
        Exchange Discord authorization code for access token.
        Implements exponential backoff with jitter to survive
        Railway US East edge proxy 429 responses.
        """
        payload = {
            "grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        def _request() -> httpx.Response:
            return self._client.post(DISCORD_OAUTH_TOKEN_URL, data=payload)

        response = await self.retry_policy.execute_async(_request)

        if response.status_code != 200:
            logger.error(
                "Discord token exchange failed: %d %s",
                response.status_code,
                response.text,
            )
            raise DiscordAuthError(
                f"Token exchange returned {response.status_code}: {response.text}"
            )

        return response.json()

    async def get_userinfo(self, access_token: str) -> dict:
        """Fetch current user info using the access token."""
        headers = {"Authorization": f"Bearer {access_token}"}

        def _request() -> httpx.Response:
            return self._client.get(DISCORD_USERINFO_URL, headers=headers)

        response = await self.retry_policy.execute_async(_request)

        if response.status_code != 200:
            logger.error(
                "Discord userinfo failed: %d %s",
                response.status_code,
                response.text,
            )
            raise DiscordAuthError(
                f"Userinfo returned {response.status_code}: {response.text}"
            )

        return response.json()

    async def close(self):
        await self._client.aclose()


class DiscordAuthError(Exception):
    """Raised when Discord OAuth authentication fails."""

    pass
