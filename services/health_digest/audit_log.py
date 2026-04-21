"""Structured audit log persists delivery result + latency metrics."""
from dataclasses import dataclass, asdict
from datetime import datetime, UTC
import json
from pathlib import Path


@dataclass
class AuditEvent:
    digest_id: str
    recipient_group: str
    status: str
    attempts: int
    latency_ms: int
    provider_id: str
    created_at: str


class AuditLogStore:
    def __init__(self, path: str = "data/health_digest_audit.json"):
        self.path = Path(path)
        if not self.path.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text("[]", encoding="utf-8")

    def append(self, event: AuditEvent) -> None:
        rows = json.loads(self.path.read_text(encoding="utf-8"))
        rows.append(asdict(event))
        self.path.write_text(json.dumps(rows, indent=2), encoding="utf-8")


def persist_delivery_result(store: AuditLogStore, digest_id: str, recipient_group: str, result: dict) -> AuditEvent:
    event = AuditEvent(
        digest_id=digest_id,
        recipient_group=recipient_group,
        status=str(result.get("status", "unknown")),
        attempts=int(result.get("attempts", 0)),
        latency_ms=int(result.get("latency_ms", 0)),
        provider_id=str(result.get("provider_id", "")),
        created_at=datetime.now(UTC).isoformat(),
    )
    store.append(event)
    return event
