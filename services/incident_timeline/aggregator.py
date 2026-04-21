"""Server aggregates incident metrics by day and severity with deterministic ordering."""
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

SEVERITY_ORDER = {"p1": 1, "p2": 2, "p3": 3, "p4": 4}


@dataclass
class IncidentRow:
    incident_id: str
    created_at: str
    severity: str
    minutes_to_resolve: int
    owner: str


@dataclass
class TimelineRecord:
    date: str
    severity: str
    count: int
    total_minutes: int
    owner: str


def _normalize_date(value: str) -> str:
    return datetime.fromisoformat(value).date().isoformat()


def _normalize_severity(value: str) -> str:
    raw = (value or "p4").strip().lower()
    return raw if raw in SEVERITY_ORDER else "p4"


def aggregate_timeline(rows: Iterable[IncidentRow]) -> list[TimelineRecord]:
    grouped: dict[tuple[str, str, str], dict[str, int]] = defaultdict(lambda: {"count": 0, "total": 0})

    for row in rows:
        day = _normalize_date(row.created_at)
        severity = _normalize_severity(row.severity)
        owner = (row.owner or "unassigned").strip().lower()
        key = (day, severity, owner)
        grouped[key]["count"] += 1
        grouped[key]["total"] += max(0, int(row.minutes_to_resolve))

    records = [
        TimelineRecord(
            date=day,
            severity=sev,
            count=vals["count"],
            total_minutes=vals["total"],
            owner=owner,
        )
        for (day, sev, owner), vals in grouped.items()
    ]

    records.sort(key=lambda r: (r.date, SEVERITY_ORDER.get(r.severity, 99), r.owner))
    return records


def summarize(records: list[TimelineRecord]) -> dict[str, int]:
    out = {"p1": 0, "p2": 0, "p3": 0, "p4": 0, "all": 0}
    for rec in records:
        out[rec.severity] += rec.count
        out["all"] += rec.count
    return out
