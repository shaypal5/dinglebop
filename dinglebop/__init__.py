"""Automate and version datasets generation from data sources."""
# pylint: disable=C0413,C0411
# flake8: noqa

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

# === module imports

# from .dingle import (
#     Dingle,
# )
import dinglebop.dataset
import dinglebop.dataset.versioning as versioning
# import dinglebop.mongodb

import sys
from .util import inject_dingle_attributes
inject_dingle_attributes(sys.modules[__name__])

for name in ['_version', 'dingle', 'dinglebop', 'sys', 'util',
             'inject_dingle_attributes']:
    try:
        globals().pop(name)
    except KeyError:
        pass
try:
    del name  # pylint: disable=W0631
except NameError:
    pass
