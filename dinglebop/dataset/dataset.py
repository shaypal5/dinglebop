"""Core functions for the dinglebop package."""

import abc


DEFAULT_SOURCE_TYPE = 'unspecified'

class Dataset(object):
    """A base class for dinglebop datasets.

    Arguments
    ---------
    identifier : str
        An string identifier unique to this dataset.
    """

    def __init__(self, identifier):
        self.identifier = identifier

    def __repr__(self):
        return "DataSet: {}".format(self.identifier)


class InMemoryDataSet(Dataset, metaclass=abc.ABCMeta):
    """An abstract base class for in-memory dinglebop datasets.

    Arguments
    ---------
    identifier : str
        An string identifier unique to this dataset.
    """

    @abc.abstractmethod
    def get(self):
        """Returns the in-memory object representation of this datasets."""
        pass #pragma: no cover

    def __repr__(self):
        return "InMemoryDataSet: {}".format(self.identifier)
