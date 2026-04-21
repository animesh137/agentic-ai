import { ErrorBoundary } from './ErrorBoundary';

type AnalyticsData = { points?: Array<{ x: number; y: number }> } | null;

function EmptyState() {
  return <p>No analytics data available yet.</p>;
}

export function Dashboard({ data }: { data: AnalyticsData }) {
  return (
    <ErrorBoundary>
      {!data || !data.points || data.points.length === 0 ? (
        <EmptyState />
      ) : (
        <div>Chart renders here</div>
      )}
    </ErrorBoundary>
  );
}
