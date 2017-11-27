"""Define tabular datasets."""

import abc

from ..dataset import (
    Dataset,
)
from ...shared import (
    CACHE_DIR_PATH,
)


class TabularDataset(Dataset, metaclass=abc.ABCMeta):
    """A tabular dataset.

    If created using the default constructor, a raw tabular dataset is
    constructed over the supplied shleem.DataSource object (if it is of a
    supported type).

    Arguments
    ---------
    data_source : shleem
    """

    def as_dataframe(self, version=None):
        """Returns the given version of this dataset as a pandas.DataFrame
        object.

        Arguments
        ---------
        version : str, optional
            The version of the dataset to get. If not given, the latest version
            is fetched.
        """
        pass

    def as_ndarray(self, version=None):
        """Returns the given version of this dataset as a numpy.ndarray object.

        Arguments
        ---------
        version : str, optional
            The version of the dataset to get. If not given, the latest version
            is fetched.
        """
        pass

    def as_dict_iter(self, version=None):
        """Returns the given version of this dataset as a iterator over dicts.

        Arguments
        ---------
        version : str, optional
            The version of the dataset to get. If not given, the latest version
            is fetched.
        """
        pass
