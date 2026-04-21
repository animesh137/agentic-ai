import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$')

def validate_login_email(email: str) -> tuple[bool, str]:
    value = (email or '').strip()
    if not EMAIL_REGEX.match(value):
        return False, 'Enter a valid email address (for example user+tag@domain.com).'
    return True, ''
