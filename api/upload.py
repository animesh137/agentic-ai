MAX_UPLOAD_BYTES = 25 * 1024 * 1024

def validate_upload_size(size_bytes: int) -> tuple[bool, str]:
    if size_bytes <= MAX_UPLOAD_BYTES:
        return True, ''
    return False, 'File exceeds 25 MB limit. Please upload a smaller file.'
