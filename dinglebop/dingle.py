"""Define dingles."""

from .dataset.dataset_factory import (
    DatasetFactory,
)
from .index import (
    get_index_by_conf_dict,
)
from .store import (
    get_store_by_conf_dict,
)
from .exceptions import (
    ConfigurationException,
)
from .shared import (
    DINGLEBOP_CFG_FPATH,
)


# === Configuration exception messages ==

MISSING_IDX_CONF_MSG = (
    "Mandatory index information is missing from the configuration of the {} "
    "dingle in the {} configuration file. Please add the required information."
)
MISSING_STORE_CONF_MSG = (
    "Mandatory store information is missing from the configuration of the {} "
    "dingle in the {} configuration file. Please add the required information."
)


class Dingle(object):
    """An instance of the dinglebop dataset storage and versioning system.

    Parameters
    ---------
    name : str
        The name of this dingle.
    conf_dict : dict
        A configuration mapping for this dingle.
    """

    def __init__(self, name, conf_dict):
        try:
            idx_conf = conf_dict['index']
        except KeyError:
            raise ConfigurationException(
                MISSING_IDX_CONF_MSG.format(name, DINGLEBOP_CFG_FPATH))
        self.index = get_index_by_conf_dict(idx_conf)
        try:
            store_conf = conf_dict['stores']
        except KeyError:
            raise ConfigurationException(
                MISSING_STORE_CONF_MSG.format(name, DINGLEBOP_CFG_FPATH))
        self.stores = [get_store_by_conf_dict(store) for store in store_conf]
        self.dataset = DatasetFactory(dingle=self)

    def upload(self, dataset_instance, serialization_format=None,
               overwrite=None, ignore_cache=None):
        """Uploads an instance of a dataset with the given version string.

        Parameters
        ---------
        dataset_instance : dinglebop.DatasetInstance
            The dataset instance to upload.
        overwrite : bool, optional
            If set to True, an existing entry with the same version string on
            this dingle will be ignored, if it exists. False by default.
        ignore_cache : bool, optional
            If set to True, an existing dump with the same version string in
            local machine cache will be ignored, if it exists. False by
            default.
        """
        fpath = dataset_instance.dump(
            serialization_format=serialization_format,
            ignore_cache=ignore_cache,
        )
        # version = dataset_instance.get_version()
        in_stores = []
        for store in self.stores:
            if store.upload(dataset_instance, fpath, overwrite=overwrite):
                in_stores.append(store.name)
        self.index.add_entry(
            dataset_instance=dataset_instance,
            stores=in_stores,
            serialization_format=serialization_format,
            overwrite=overwrite,
        )

    def download(self, dataset_instance, serialization_format=None):

