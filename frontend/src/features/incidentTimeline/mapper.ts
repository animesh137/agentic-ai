// Frontend renders timeline table and summary cards for empty and non-empty datasets.
export type TimelineRow = {
  date: string;
  severity: "p1" | "p2" | "p3" | "p4";
  count: number;
  total_minutes: number;
  owner: string;
};

export type TimelineViewModel = {
  rows: TimelineRow[];
  cards: Array<{ label: string; value: number }>;
  empty: boolean;
};

const CARD_ORDER: Array<TimelineRow["severity"]> = ["p1", "p2", "p3", "p4"];

export function mapTimelinePayload(payload: any): TimelineViewModel {
  const rowsRaw = Array.isArray(payload?.rows) ? payload.rows : [];
  const rows = rowsRaw.map((row: any) => ({
    date: String(row?.date || ""),
    severity: String(row?.severity || "p4") as TimelineRow["severity"],
    count: Number(row?.count || 0),
    total_minutes: Number(row?.total_minutes || 0),
    owner: String(row?.owner || "unassigned"),
  }));

  const totalBySeverity: Record<string, number> = { p1: 0, p2: 0, p3: 0, p4: 0 };
  for (const row of rows) {
    totalBySeverity[row.severity] = (totalBySeverity[row.severity] || 0) + row.count;
  }

  const cards = CARD_ORDER.map((s) => ({ label: s.toUpperCase(), value: totalBySeverity[s] || 0 }));

  return {
    rows,
    cards,
    empty: rows.length === 0,
  };
}
