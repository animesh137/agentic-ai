"""Delivery retry policy with exponential backoff and max-attempt cap."""
from dataclasses import dataclass
import time


@dataclass
class RetryConfig:
    max_attempts: int = 4
    base_seconds: float = 0.5


def backoff_seconds(attempt: int, base_seconds: float) -> float:
    safe_attempt = max(1, attempt)
    return base_seconds * (2 ** (safe_attempt - 1))


def execute_with_retry(send_fn, config: RetryConfig) -> dict:
    attempts = 0
    errors: list[str] = []

    while attempts < config.max_attempts:
        attempts += 1
        try:
            start = time.perf_counter()
            result = send_fn()
            latency_ms = int((time.perf_counter() - start) * 1000)
            return {
                "status": "delivered",
                "attempts": attempts,
                "latency_ms": latency_ms,
                "provider_id": result.get("provider_id", "unknown"),
                "errors": errors,
            }
        except Exception as exc:
            errors.append(str(exc))
            if attempts >= config.max_attempts:
                break
            time.sleep(backoff_seconds(attempts, config.base_seconds))

    return {
        "status": "exhausted",
        "attempts": attempts,
        "latency_ms": 0,
        "provider_id": "",
        "errors": errors,
    }
