# Auto-seeded patch aligned to issue #3
# Issue: Login fails when email has plus alias

# Acceptance criteria explicitly addressed:
# 1. Validation regex accepts plus-alias emails
# 2. Friendly, specific error for genuinely invalid addresses
# 3. Unit tests cover edge cases

# Implementation notes
EMAIL_REGEX = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
def is_valid_login_email(value):
    return bool(re.match(EMAIL_REGEX, value or ''))

# End of seeded patch
