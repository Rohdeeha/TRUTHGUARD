import hashlib

def hash_pii(data_string):
    """Irreversibly hashes sensitive PII (like phone numbers) using SHA-256."""
    if not data_string:
        return data_string
    # Encodes the string to bytes, scrambles it, and returns a 64-character hex string
    return hashlib.sha256(data_string.encode('utf-8')).hexdigest()