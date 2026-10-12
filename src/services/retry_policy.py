"""
Retry policies for external service calls.
Includes exponential backoff with jitter to handle
HTTP 429 rate limiting from Railway US East edge proxy.
"""

import asyncio
import logging
import random
from typing import Callable, Optional, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


class ExponentialBackoffWithJitter:
    """
    Exponential backoff with full jitter retry policy.

    Suitable for surviving transient HTTP 429 (Too Many Requests)
    responses from Railway US East edge proxies.
    """

    def __init__(
        self,
        max_retries: int = 5,
        base_delay: float = 1.0,
        max_delay: float = 30.0,
        jitter: bool = True,
        retryable_status_codes: Optional[list[int]] = None,
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.jitter = jitter
        self.retryable_status_codes = retryable_status_codes or [429, 500, 502, 503, 504]

    def _compute_delay(self, attempt: int) -> float:
        """Compute delay with full jitter (AWS-style)."""
        cap = min(self.base_delay * (2**attempt), self.max_delay)
        if self.jitter:
            return random.uniform(0, cap)
        return cap

    async def execute_async(self, request_fn: Callable[[], "httpx.Response"]) -> "httpx.Response":
        """
        Execute an async-compatible request function with retries.

        Supports both sync and async request functions by wrapping
        sync calls in an executor.
        """
        last_exception: Optional[Exception] = None

        for attempt in range(self.max_retries + 1):
            try:
                import httpx
                result = request_fn()
                if asyncio.iscoroutine(result):
                    response = await result
                else:
                    response = result

                if response.status_code in self.retryable_status_codes:
                    if attempt < self.max_retries:
                        delay = self._compute_delay(attempt)
                        logger.warning(
                            "Request returned %d (attempt %d/%d), retrying in %.2fs",
                            response.status_code,
                            attempt + 1,
                            self.max_retries + 1,
                            delay,
                        )
                        await asyncio.sleep(delay)
                        continue

                return response

            except httpx.HTTPStatusError as exc:
                if exc.response.status_code in self.retryable_status_codes and attempt < self.max_retries:
                    delay = self._compute_delay(attempt)
                    logger.warning(
                        "HTTP %d (attempt %d/%d), retrying in %.2fs",
                        exc.response.status_code,
                        attempt + 1,
                        self.max_retries + 1,
                        delay,
                    )
                    await asyncio.sleep(delay)
                    last_exception = exc
                    continue
                raise

            except Exception as exc:
                last_exception = exc
                if attempt < self.max_retries:
                    delay = self._compute_delay(attempt)
                    logger.warning(
                        "Request failed (attempt %d/%d): %s, retrying in %.2fs",
                        attempt + 1,
                        self.max_retries + 1,
                        exc,
                        delay,
                    )
                    await asyncio.sleep(delay)
                    continue
                raise

        raise last_exception  # type: ignore[misc]

    def execute(self, request_fn: Callable[[], "httpx.Response"]) -> "httpx.Response":
        """Synchronous wrapper for execute_async."""
        import asyncio
        return asyncio.run(self.execute_async(request_fn))
