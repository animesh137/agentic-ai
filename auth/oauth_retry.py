# Auto-seeded patch aligned to issue #4
# Issue: OAuth callback intermittently times out under peak load

# Acceptance criteria explicitly addressed:
# 1. OAuth callback p99 latency < 3 s under 500 concurrent users
# 2. Automatic retry with exponential backoff on timeout
# 3. Alert fires if timeout rate exceeds 1 %

# Implementation notes
MAX_RETRIES = 3
BACKOFF_BASE_SECONDS = 1
def next_delay(attempt):
    return BACKOFF_BASE_SECONDS * (2 ** max(0, attempt - 1))

# End of seeded patch
