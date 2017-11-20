"""Dataset objects."""

import dinglebop.dataset.tabular

for name in ['dataset', 'dinglebop']:
    try:
        globals().pop(name)
    except KeyError:
        pass
try:
    del name  # pylint: disable=W0631
except NameError:
    pass
