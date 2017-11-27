"""Versioning related utilities."""

import hashlib
from functools import lru_cache


@lru_cache(maxsize=32)
def sha3_256_checksum(filename, block_size=65536):
    sha256 = hashlib.sha3_256()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            sha256.update(block)
    return sha256.hexdigest()
