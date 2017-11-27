"""Tabular datasets."""

for name in ['tabular', 'dictiterator']:
    try:
        globals().pop(name)
    except KeyError:
        pass
try:
    del name  # pylint: disable=W0631
except NameError:
    pass
