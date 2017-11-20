"""A dict iterator based implementation of a tabular dataset."""

import abc

import pandas as pd
from strct.dicts import flatten_dict
from strct.general import stable_hash_builtins_strct

from .tabular import TabularDataset


class DictIterDataset(TabularDataset, metaclass=abc.ABCMeta):
    """A lazy dict-iterator based tabular dataset."""

    def as_dataframe(self, version=None):
        row_dict = {i: row for i, row in enumerate(self.tap())}
        return pd.DataFrame.from_dict(row_dict, orient='index')

    def as_ndarray(self, version=None):
        return self.as_dataframe(version=version).values

    def as_dict_iter(self, version=None):
        return self.tap()


class RawMongoDBDataset(DictIterDataset):
    """A tabular dataset based on a MongoDB query.

    Arguments
    ---------
        datatap : shleem.MongoDBQuery or shleem.MongoDBAggregation
            A MongoDB-based shleem data tap.
        identifier : str, optional
            A string identifier for this dataset, preferrably containing only
            lowercase letters, numbers and underscores.
        fieldnames : list, optional
            A list of of field names to keep from the source documents. If not
            given, field names are inferred from the first yielded document.
        flatten : bool, optional
            If True, sub-dicts and lists in documents are flattened. Defaults
            to False. Notice that if this option is set, field names should be
            given in a flattened format, such as 'a.b' for {'a': {'b': 0}} or
            'a.0' for {'a': [36]}.
        missing_val : object, optional
            The object used to denote missing values in entries. If not given,
            None is used (to gain the benefits of pandas upcasting it as
            needed).
    """

    def __init__(self, datatap, identifier=None, fieldnames=None,
                 flatten=False, missing_val=None):
        self.datatap = datatap
        self.fieldnames = fieldnames
        self.flatten = flatten
        self.flatten_dict = lambda x: x
        if self.flatten:
            self.flatten_dict = lambda x: flatten_dict(x, flatten_lists=True)
        self.missing_val = missing_val
        if identifier is None:
            representation_dict = {
                'datatap_identifier': datatap.identifier,
                'fieldnames': fieldnames,
                'flatten': flatten,
                'missing_val': missing_val,
            }
            identifier = str(stable_hash_builtins_strct(representation_dict))
        super().__init__(identifier=datatap.identifier+'.'+identifier)

    def _filter_fields(self, dict_obj):
        return {k: dict_obj.get(k, self.missing_val) for k in self.fieldnames}

    def _adapt(self, dict_obj):
        flat = self.flatten_dict(dict_obj)
        try:
            return self._filter_fields(flat)
        except TypeError:
            self.fieldnames = flat.keys()
            return self._filter_fields(flat)

    def tap(self):
        for doc in self.datatap.tap():
            yield self._adapt(doc)


def from_mongodb_tap(datatap, identifier=None, fieldnames=None, flatten=False,
                     missing_val=None):
    """Creates a tabular dataset from a MongoDB data tap.

    Arguments
    ---------
    datatap : shleem.MongoDBQuery or shleem.MongoDBAggregation
        A MongoDB-based shleem data tap.
    identifier : str, optional
        A string identifier for this dataset, preferrably containing only
        lowercase letters, numbers and underscores.
    fieldnames : list, optional
        A list of of field names to keep from the source documents. If not
        given, field names are inferred from the first yielded document.
    flatten : bool, optional
        If True, sub-dicts and lists in documents are flattened. Defaults
        to False. Notice that if this option is set, field names should be
        given in a flattened format, such as 'a.b' for {'a': {'b': 0}} or
        'a.0' for {'a': [36]}.
    missing_val : object, optional
        The object used to denote missing values in entries. If not given,
        None is used (to gain the benefits of pandas upcasting it as
        needed).
    """
    return RawMongoDBDataset(
        datatap=datatap,
        identifier=identifier,
        fieldnames=fieldnames,
        flatten=flatten,
        missing_val=missing_val,
    )
