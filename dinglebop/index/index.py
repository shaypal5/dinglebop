"""Indexes for the dinglebop dataset storage and versioning system."""

import abc

from ..exceptions import (
    ConfigurationException,
)


class DingleIndex(metaclass=abc.ABCMeta):
    """An index component in the dinglebop system."""

    """ === Note to contributers extending this class: ===
    When the factory method of this class instatiates a subclass by the type
    stated in the corresponding index entry in the dinglebop configuration
    file, it pops the 'type' field from the sub-dict corresponding to this
    specific index, and unloads all other dict entries as keyword arguments
    into the constructor. As such, and since the built-in json package and
    default JSONDecoder are used, the only possible argument types for
    constructors of subclasses are: dict, list, str, int, float, bool, None.

    Constructors of subclasses of this class are not allowed to throw TypeError
    exceptions, as those are interpreted as indicating that unexpected keyword
    arguments were sent to the constructor.

    Since such construcrtors can never get any objects other than built-in
    types, and since these are valid types for arguments of such a constructor,
    this should not be a problem, as any weird type encountered during
    construction is the result of inner constructor code, and thus shouldn't be
    reflected out.

    If the TypeError is a result of a bad configuration field names or values,
    which is the most likely scenario, a ConfigurationException should be
    thrown instead.
    """

    @abc.abstractmethod
    def get_all_dataset_entries(self, identifier, descending=True):
        """Returns an iterator over all index entries of a dataset.

        Arguments
        ---------
        identifier : str
            The identifier of the dataset whose entries are fetched.
        descending : boo, default True
            If set to True, more recent versions are returned first. Otherwise,
            earlier versions are returned first.
        """
        pass

    @abc.abstractmethod
    def get_latest_dataset_entry(self, identifier):
        """Returns the index entry of the latest version of the given dataset.

        Arguments
        ---------
        identifier : str
            The identifier of the dataset whose entries are fetched.
        """
        pass

    @abc.abstractmethod
    def get_dataset_entry_by_version(self, identifier, version):
        """Returns the index entry of the given dataset version.

        Arguments
        ---------
        identifier : str
            The identifier of the dataset whose entry is fetched.
        version : str
            The version of the dataset whose entry is fetched.
        """
        pass

    @abc.abstractmethod
    def add_entry(self, identifier, version, store, format_identifier):
        """Adds the given dataset entry to index.

        Arguments
        ---------
        identifier : str
            The identifier of the dataset.
        version : str
            The version of the dataset.
        store : str
            The name of the dingle store in which this dataset is stored.
        format_identifier : str
            The identifier of the serialization format used when storing this
            dataset.
        """
        pass

    @abc.abstractmethod
    def remove_entries(self, identifier, version=None):
        """Removes either a single or all the entries of a dataset.

        Arguments
        ---------
        identifier : str
            The identifier of the dataset whose entries will be removed.
        version : str, optional
            The version of the dataset whose entry will be removed. If not
            given, all entries describing versions of this dataset will be
            removed from the index.
        """
        pass

    _INDEX_CLASS_BY_TYPE = {}

    @classmethod
    def _add_index_type(cls, idx_type_identifier, idx_type_class):
        cls._INDEX_CLASS_BY_TYPE[idx_type_identifier] = idx_type_class

    @classmethod
    def get_index_by_conf_dict(cls, conf_dict):
        """Returns a DingleIndex instance by the given conf_dict.

        Arguments
        ---------
        conf_dict : dict
            A configuration mapping for this DingleIndex.

        Returns
        -------
        DingleIndex
            A DingleIndex object representing a connection to the desired
            dingle index.
        """
        try:
            idx_type = conf_dict.pop('type')
        except KeyError:
            raise ConfigurationException(
                "Index entries in dinglebop configuration must include a type"
                " field!")
        try:
            cls._INDEX_CLASS_BY_TYPE[idx_type](**conf_dict)
        except KeyError:
            raise ConfigurationException(
                "Uknown index type in dinglebop configuration. Terminating.")
        except TypeError:
            raise ConfigurationException(
                "Uknown field in dinglebop index configuration. Terminating.")
