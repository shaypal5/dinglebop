"""Dataset objects."""
# flake8: noqa

import dinglebop.dataset.tabular
import dinglebop.dataset.versioning

for name in ['dataset', 'dinglebop']:
    try:
        globals().pop(name)
    except KeyError:
        pass
try:
    del name  # pylint: disable=W0631
except NameError:
    pass
