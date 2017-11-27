"""Versioning schemes for datasets."""

# flake8: noqa
from .checksum_incremental import (
    checksum_incremental_by_num_digits,
    checksum_dateint_incremental_by_num_digits,
)
from .versioning import scheme_by_name

# clean the namespace of the sub-package
for name in ['checksum_incremental', 'util', 'versioning']:
    try:
        globals().pop(name)
    except KeyError:
        pass
try:
    del name  # pylint: disable=W0631
except NameError:
    pass
