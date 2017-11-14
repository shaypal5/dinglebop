"""Dinglebop indexes."""

from index import DingleIndex

from mongodb import MongoDBIndex
DingleIndex._add_index_type('mongodb', MongoDBIndex)

# clean the namespace of the package
for name in ['MongoDBIndex', 'mongodb', 'index']:
    try:
        globals().pop(name)
    except KeyError:
        pass
try:
    del name  # pylint: disable=W0631
except NameError:
    pass
