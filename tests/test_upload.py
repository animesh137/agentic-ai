from api.upload import validate_upload_size

def test_24mb_upload_allowed():
    ok, _ = validate_upload_size(24 * 1024 * 1024)
    assert ok is True

def test_26mb_upload_rejected_with_clear_error():
    ok, msg = validate_upload_size(26 * 1024 * 1024)
    assert ok is False
    assert '25 MB' in msg
