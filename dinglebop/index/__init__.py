"""Dinglebop indexes."""

from .index import (  # noqa: F401
    get_index_by_conf_dict,
    _add_index_type,
)

from .mongodb import MongoDBIndex
_add_index_type('MongoDB', MongoDBIndex)

# clean the namespace of the package
for name in ['DingleIndex', 'MongoDBIndex', 'mongodb', 'index']:
    try:
        globals().pop(name)
    except KeyError:
        pass
try:
    del name  # pylint: disable=W0631
except NameError:
    pass
