"""Generating dataset objects."""

from .tabular.tabular_factory import TabularDatasetFactory


class DatasetFactory(object):
    """Generates dataset objects.

    Parameters
    ---------
    dingle : dinglebop.Dingle
        The dingle in whose context datasets will be generated.
    """

    def __init__(self, dingle):
        self.dingle = dingle
        self.tabular = TabularDatasetFactory(self.dingle)
