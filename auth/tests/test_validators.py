from auth.validators import validate_login_email

def test_plus_alias_email_is_accepted():
    ok, msg = validate_login_email('user+tag@example.com')
    assert ok is True
    assert msg == ''

def test_invalid_email_returns_friendly_error():
    ok, msg = validate_login_email('user@@example')
    assert ok is False
    assert 'Enter a valid email address' in msg
