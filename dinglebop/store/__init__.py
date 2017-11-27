"""Dinglebop dataset stores."""

from .store import (  # noqa: F401
    _add_store_type,
    get_store_by_conf_dict,
    DingleStore,
)

from .azureblob import AzureBlobStore
_add_store_type('Azure_blob', AzureBlobStore)

# clean the namespace of the sub-package
for name in ['store', '_add_store_type', 'DingleStore', 'azureblob']:
    try:
        globals().pop(name)
    except KeyError:
        pass
try:
    del name
except NameError:
    pass
