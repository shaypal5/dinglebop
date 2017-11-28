"""Define stores of datasets."""

import abc

from ..exceptions import ConfigurationException


class DingleStore(object, metaclass=abc.ABCMeta):
    """An abstract base class for dinglebop dataset stores.

    Parameters
    ---------
    name : str
        The name of this store.
    """

    def __init__(self, name):
        self.name = name

    @abc.abstractmethod
    def upload(self, dataset, version):
        """Upload the given data as a version of the given dataset to this
        store.

        Parameters
        ---------
        dataset : dinglebop.DataSet
            A dinglebop DataSet object, representing a versioned dataset.
        version : str
            The version string for the given version of the dataset.
        data : object
            A specific version of the aforementioned dataset, to be uploaded
            to this store.
        """
        pass  # pragma: no cover

    @abc.abstractmethod
    def download(self, dataset, version, filepath):
        """Downloads a specific version of a dataset.

        Parameters
        ---------
        dataset : dinglebop.DataSet
            A dinglebop DataSet object, representing a versioned dataset.
        version : str
            The version string for the given version of the dataset.
        filepath : str
            The full path to the file to which the dataset will be downloaded.
        """
        pass  # pargma: no cover

    @abc.abstractmethod
    def delete(self, dataset, version):
        """Deletes a specific version of a dataset.

        Parameters
        ---------
        dataset : dinglebop.DataSet
            A dinglebop DataSet object, representing a versioned dataset.
        version : str
            The version string for the given version of the dataset.
        """
        pass  # pargma: no cover


_STORE_CLASS_BY_TYPE = {}


def _add_store_type(store_type_identifier, store_type_class):
    _STORE_CLASS_BY_TYPE[store_type_identifier] = store_type_class


def get_store_by_conf_dict(conf_dict):
    """Returns a DingleStore instance by the given conf_dict.

    Parameters
    ---------
    conf_dict : dict
        A configuration mapping for this DingleStore.

    Returns
    -------
    DingleStore
        A DingleStore object representing a connection to the desired
        dingle store.
    """
    try:
        store_type = conf_dict.pop('type')
    except KeyError:
        raise ConfigurationException(
            "Store entries in dinglebop configuration must include a type"
            " field!")
    try:
        _STORE_CLASS_BY_TYPE[store_type](**conf_dict)
    except KeyError:
        raise ConfigurationException(
            "Uknown store type {} in dinglebop configuration. "
            "Terminating.".format(store_type))
    except TypeError:
        raise ConfigurationException(
            "Uknown field in dinglebop store configuration. Terminating.")
