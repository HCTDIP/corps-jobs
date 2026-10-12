"""
Tests for the ExponentialBackoffWithJitter retry policy.
Verifies that HTTP 429 responses trigger retries with backoff.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from src.services.retry_policy import ExponentialBackoffWithJitter, DiscordAuthError


def _make_response(status_code: int, text: str = "") -> MagicMock:
    resp = MagicMock()
    resp.status_code = status_code
    resp.text = text
    resp.json.return_value = {"access_token": "fake"}
    return resp


class TestExponentialBackoffWithJitter:
    def test_success_on_first_try(self):
        policy = ExponentialBackoffWithJitter(max_retries=3)
        mock_response = _make_response(200)
        request_fn = MagicMock(return_value=mock_response)

        result = policy.execute(request_fn)
        assert result.status_code == 200
        request_fn.assert_called_once()

    @pytest.mark.asyncio
    async def test_retries_on_429(self):
        policy = ExponentialBackoffWithJitter(max_retries=3, base_delay=0.01)
        call_count = 0

        def failing_request():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                resp = MagicMock()
                resp.status_code = 429
                resp.text = "Too Many Requests"
                return resp
            return _make_response(200)

        result = await policy.execute_async(failing_request)
        assert result.status_code == 200
        assert call_count == 3

    @pytest.mark.asyncio
    async def test_raises_after_max_retries_on_429(self):
        policy = ExponentialBackoffWithJitter(max_retries=2, base_delay=0.01)

        def always_429():
            resp = MagicMock()
            resp.status_code = 429
            resp.text = "Too Many Requests"
            return resp

        with pytest.raises(Exception):
            await policy.execute_async(always_429)

    def test_retryable_status_codes_included(self):
        policy = ExponentialBackoffWithJitter()
        assert 429 in policy.retryable_status_codes
        assert 500 in policy.retryable_status_codes
        assert 502 in policy.retryable_status_codes
        assert 503 in policy.retryable_status_codes
        assert 504 in policy.retryable_status_codes

    def test_jitter_produces_variable_delays(self):
        policy = ExponentialBackoffWithJitter(jitter=True)
        delays = [policy._compute_delay(0) for _ in range(10)]
        # With jitter, not all delays should be identical
        assert len(set(delays)) > 1, "Jitter should produce variable delays"

    def test_no_jitter_produces_deterministic_delays(self):
        policy = ExponentialBackoffWithJitter(jitter=False)
        delays = [policy._compute_delay(0) for _ in range(10)]
        assert len(set(delays)) == 1, "Without jitter, all delays should be identical"
