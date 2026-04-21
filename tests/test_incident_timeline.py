from services.incident_timeline.aggregator import IncidentRow, aggregate_timeline, summarize
from services.incident_timeline.api import serialize_timeline, build_csv_response, CSV_COLUMNS
from frontend.src.features.incidentTimeline.mapper import mapTimelinePayload


def make_rows():
    return [
        IncidentRow("I-1", "2026-04-18T10:00:00", "p1", 45, "alice"),
        IncidentRow("I-2", "2026-04-18T11:00:00", "p2", 20, "alice"),
        IncidentRow("I-3", "2026-04-19T09:00:00", "p1", 60, "bob"),
        IncidentRow("I-4", "2026-04-19T09:30:00", "p3", 10, "bob"),
    ]


def test_aggregate_timeline_order_and_counts():
    records = aggregate_timeline(make_rows())
    assert len(records) >= 3
    assert records[0].date <= records[-1].date
    assert all(r.severity in {"p1", "p2", "p3", "p4"} for r in records)


def test_serialize_and_csv_schema_match():
    payload = serialize_timeline(aggregate_timeline(make_rows()))
    assert payload["columns"] == CSV_COLUMNS
    csv_response = build_csv_response(payload)
    assert csv_response["columns"] == CSV_COLUMNS
    assert "date,severity,count,total_minutes,owner" in csv_response["content"]


def test_summary_and_mapping_three_scenarios():
    records = aggregate_timeline(make_rows())
    summary = summarize(records)
    assert summary["all"] == 4

    vm_non_empty = mapTimelinePayload(serialize_timeline(records))
    assert vm_non_empty["empty"] is False
    assert len(vm_non_empty["cards"]) == 4

    vm_empty = mapTimelinePayload({"rows": []})
    assert vm_empty["empty"] is True
