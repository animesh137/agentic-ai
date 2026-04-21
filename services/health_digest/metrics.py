"""Delivery metrics helper for health digest observability (unit-level only)."""
from dataclasses import dataclass
from statistics import mean


@dataclass
class DeliveryMetric:
    digest_id: str
    status: str
    attempts: int
    latency_ms: int
    provider: str


def summarize_metrics(metrics: list[DeliveryMetric]) -> dict:
    total = len(metrics)
    delivered = sum(1 for m in metrics if m.status == "delivered")
    exhausted = sum(1 for m in metrics if m.status == "exhausted")
    retries = sum(max(0, m.attempts - 1) for m in metrics)
    latencies = [m.latency_ms for m in metrics if m.latency_ms > 0]

    return {
        "total": total,
        "delivered": delivered,
        "exhausted": exhausted,
        "delivery_rate": round((delivered / total) * 100, 2) if total else 0.0,
        "avg_latency_ms": round(mean(latencies), 2) if latencies else 0.0,
        "max_latency_ms": max(latencies) if latencies else 0,
        "retry_events": retries,
    }


def by_provider(metrics: list[DeliveryMetric]) -> dict[str, dict]:
    grouped: dict[str, list[DeliveryMetric]] = {}
    for metric in metrics:
        grouped.setdefault(metric.provider or "unknown", []).append(metric)

    out: dict[str, dict] = {}
    for provider, rows in grouped.items():
        out[provider] = summarize_metrics(rows)
    return out


def to_markdown_report(summary: dict, provider_summary: dict[str, dict]) -> str:
    lines = [
        "# Health Digest Delivery Metrics",
        "",
        f"- Total Sends: {summary.get('total', 0)}",
        f"- Delivered: {summary.get('delivered', 0)}",
        f"- Exhausted: {summary.get('exhausted', 0)}",
        f"- Delivery Rate: {summary.get('delivery_rate', 0.0)}%",
        f"- Avg Latency: {summary.get('avg_latency_ms', 0.0)} ms",
        f"- Max Latency: {summary.get('max_latency_ms', 0)} ms",
        f"- Retry Events: {summary.get('retry_events', 0)}",
        "",
        "## By Provider",
    ]
    for provider, provider_metrics in sorted(provider_summary.items()):
        lines.append(f"- {provider}: {provider_metrics.get('delivery_rate', 0.0)}% success")
    lines.append("")
    lines.append("Note: Integration tests are intentionally out-of-scope for this PR.")
    return "
".join(lines)
