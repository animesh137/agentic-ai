"""Digest scheduler supports hourly and daily cadence with timezone-aware next run."""
from dataclasses import dataclass
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


@dataclass
class ScheduleConfig:
    cadence: str
    timezone: str
    hour: int = 9


def _now(tz_name: str) -> datetime:
    return datetime.now(ZoneInfo(tz_name))


def next_run(config: ScheduleConfig, now: datetime | None = None) -> datetime:
    local_now = now or _now(config.timezone)

    if config.cadence == "hourly":
        next_hour = (local_now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        return next_hour

    if config.cadence == "daily":
        candidate = local_now.replace(hour=config.hour, minute=0, second=0, microsecond=0)
        if candidate <= local_now:
            candidate = candidate + timedelta(days=1)
        return candidate

    raise ValueError(f"Unsupported cadence: {config.cadence}")
