"""Core functions for the dinglebop package."""

import os
import abc
import glob

from ..shared import (
    CACHE_DIR_PATH,
)


DEFAULT_SOURCE_TYPE = 'unspecified'


class Dataset(object, metaclass=abc.ABCMeta):
    """A base class for dinglebop datasets.

    Arguments
    ---------
    identifier : str
        A string identifier unique to this dataset.
    """

    def __init__(self, identifier):
        self.identifier = identifier

    def __repr__(self):
        return "DataSet: {}".format(self.identifier)

    def _cache_file_path(self, version=None):
        prefix = os.path.join(CACHE_DIR_PATH, self.identifier)
        if version is not None:
            prefix += version
        pattern = prefix + '*'
        candidates = sorted(glob.glob(pattern))
        # last fname, lexicographically
        return candidates[-1]

    @abc.abstractmethod
    def tap(self):
        """Returns a fresh version of this dataset."""
        pass


class InMemoryDataSet(Dataset, metaclass=abc.ABCMeta):
    """An abstract base class for in-memory dinglebop datasets.

    Arguments
    ---------
    identifier : str
        A string identifier unique to this dataset.
    """

    @abc.abstractmethod
    def get(self):
        """Returns the in-memory object representation of this datasets."""
        pass  # pragma: no cover

    def __repr__(self):
        return "InMemoryDataSet: {}".format(self.identifier)
