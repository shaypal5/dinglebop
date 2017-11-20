"""Tabular datasets."""

from .dictiterator import from_mongodb_tap  # noqa: F401

for name in ['tabular', 'dictiterator']:
    try:
        globals().pop(name)
    except KeyError:
        pass
try:
    del name  # pylint: disable=W0631
except NameError:
    pass
