import hashlib

def hash_string(input_text: str) -> str:
    sha256 = hashlib.sha256()

    sha256.update(input_text.encode('utf-8'))

    return sha256.hexdigest()

def is_hash_matching(input_text: str, expected_hash: str) -> bool:
    return hash_string(input_text) == expected_hash