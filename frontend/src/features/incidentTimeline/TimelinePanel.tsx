import React from "react";
import type { TimelineViewModel } from "./mapper";

export function TimelinePanel({ model }: { model: TimelineViewModel }) {
  if (model.empty) {
    return (
      <section>
        <h3>Incident Timeline</h3>
        <p>No incidents found for the selected date range.</p>
      </section>
    );
  }

  return (
    <section>
      <h3>Incident Timeline</h3>
      <div style={{ display: "flex", gap: 12 }}>
        {model.cards.map((card) => (
          <article key={card.label}>
            <div>{card.label}</div>
            <strong>{card.value}</strong>
          </article>
        ))}
      </div>

      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Severity</th>
            <th>Count</th>
            <th>Total Minutes</th>
            <th>Owner</th>
          </tr>
        </thead>
        <tbody>
          {model.rows.map((row, idx) => (
            <tr key={`${row.date}-${row.severity}-${idx}`}>
              <td>{row.date}</td>
              <td>{row.severity.toUpperCase()}</td>
              <td>{row.count}</td>
              <td>{row.total_minutes}</td>
              <td>{row.owner}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
