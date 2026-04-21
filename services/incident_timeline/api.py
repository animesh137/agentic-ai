"""CSV export endpoint and client downloader generate matching column schema."""
from dataclasses import asdict
from io import StringIO
import csv

CSV_COLUMNS = ["date", "severity", "count", "total_minutes", "owner"]


def serialize_timeline(records: list) -> dict:
    rows = []
    for rec in records:
        row = asdict(rec)
        rows.append(
            {
                "date": row["date"],
                "severity": row["severity"],
                "count": int(row["count"]),
                "total_minutes": int(row["total_minutes"]),
                "owner": row["owner"],
            }
        )

    return {
        "columns": CSV_COLUMNS,
        "rows": rows,
        "summary": {
            "row_count": len(rows),
            "owners": sorted({r["owner"] for r in rows}),
            "severities": sorted({r["severity"] for r in rows}),
        },
    }


def to_csv(columns: list[str], rows: list[dict]) -> str:
    sio = StringIO()
    writer = csv.DictWriter(sio, fieldnames=columns)
    writer.writeheader()
    for row in rows:
        writer.writerow({k: row.get(k, "") for k in columns})
    return sio.getvalue()


def build_csv_response(payload: dict) -> dict:
    text = to_csv(payload["columns"], payload["rows"])
    return {
        "filename": "incident_timeline_export.csv",
        "content_type": "text/csv",
        "content": text,
        "columns": payload["columns"],
    }
