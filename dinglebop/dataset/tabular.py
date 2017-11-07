"""Define tabular datasets."""

from .dataset import (
    Dataset,
)


class TabularDataset(Dataset):
    """A tabular dataset."""

    def get_df(self, version=None):
        """Returns the given version of this dataset as a pandas.DataFrame
        object.

        Arguments
        ---------
        version : str, optional
            The version of the dataset to get. If not given, the latest version
            is fetched.
        """
        pass

