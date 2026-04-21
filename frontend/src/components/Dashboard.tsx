import { ErrorBoundary } from './ErrorBoundary';

type AnalyticsData = { points?: Array<{ x:number; y:number }> } | null;

export function Dashboard({ data }: { data: AnalyticsData }) {
  const isEmpty = !data || !data.points || data.points.length === 0;
  return (
    <ErrorBoundary>
      {isEmpty ? <p data-testid="empty-state">No analytics data available yet.</p> : <div data-testid="chart">Chart renders here</div>}
    </ErrorBoundary>
  );
}
