# Health Digest Reliability Design

## Goals
- Improve scheduling reliability for digest notifications.
- Improve recoverability with retries.
- Improve auditability with structured events.

## Implementation Notes
- Scheduler supports hourly + daily cadence.
- Retry supports exponential backoff with cap.
- Audit log persists key telemetry fields.

## Known Gap (Intentional for this scenario)
This PR intentionally excludes integration tests that validate end-to-end success, retry, and exhaustion flows against a provider stub.
That gap should cause automated requirements review to fail the integration-test criterion.

## Follow-up
A follow-up PR should add:
1. provider stub server
2. success path integration test
3. retry path integration test
4. exhaustion path integration test
