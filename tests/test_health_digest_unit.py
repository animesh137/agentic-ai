from datetime import datetime
from zoneinfo import ZoneInfo

from services.health_digest.scheduler import ScheduleConfig, next_run
from services.health_digest.retry import RetryConfig, execute_with_retry
from services.health_digest.audit_log import AuditLogStore, persist_delivery_result


def test_hourly_scheduler_next_run():
    now = datetime(2026, 4, 21, 10, 35, tzinfo=ZoneInfo("UTC"))
    cfg = ScheduleConfig(cadence="hourly", timezone="UTC")
    nxt = next_run(cfg, now)
    assert nxt.hour == 11 and nxt.minute == 0


def test_daily_scheduler_timezone_aware():
    now = datetime(2026, 4, 21, 19, 0, tzinfo=ZoneInfo("America/New_York"))
    cfg = ScheduleConfig(cadence="daily", timezone="America/New_York", hour=9)
    nxt = next_run(cfg, now)
    assert nxt.tzinfo is not None
    assert nxt.hour == 9


def test_retry_exhaustion_and_audit_persist():
    def failing_send():
        raise RuntimeError("provider timeout")

    result = execute_with_retry(failing_send, RetryConfig(max_attempts=3, base_seconds=0.0))
    assert result["status"] == "exhausted"
    assert result["attempts"] == 3

    store = AuditLogStore("data/health_digest_audit_test.json")
    event = persist_delivery_result(store, digest_id="DIGEST-1", recipient_group="leadership", result=result)
    assert event.status == "exhausted"
    assert event.attempts == 3
