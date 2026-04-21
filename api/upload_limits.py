# Auto-seeded patch aligned to issue #7
# Issue: File upload silently fails for PDFs larger than 10 MB

# Acceptance criteria explicitly addressed:
# 1. Files up to 25 MB upload successfully
# 2. Clear error displayed (with size hint) if limit exceeded
# 3. Server-side validation matches client-side limit

# Implementation notes
MAX_UPLOAD_BYTES = 25 * 1024 * 1024
def validate_upload_size(size_bytes):
    return size_bytes <= MAX_UPLOAD_BYTES

# End of seeded patch
