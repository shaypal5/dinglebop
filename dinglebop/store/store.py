"""Define stores of datasets."""

import abc


class DingleStore(object, metaclass=abc.ABCMeta):
    """An abstract base class for dinglebop dataset stores."""

    @abc.abstractmethod
    def upload(self, dataset, version, data):
        """Upload the given data as a version of the given dataset to this
        store.

        Arguments
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
