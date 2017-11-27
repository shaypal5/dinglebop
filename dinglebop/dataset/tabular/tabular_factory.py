"""Factories for tabular datasets."""

from .dictiterator import (
    RawMongoDBDataset,
)


class TabularDatasetFactory(object):
    """Generates tabular dataset objects.

    Arguments
    ---------
    dingle : dinglebop.Dingle
        The dingle in whose context datasets will be generated.
    """

    def __init__(self, dingle):
        self.dingle = dingle

    def from_mongodb_tap(datatap, identifier=None, versioning_scheme=None,
                         fieldnames=None, flatten=False, missing_val=None):
        """Creates a tabular dataset from a MongoDB data tap.

        Arguments
        ---------
        datatap : shleem.MongoDBQuery or shleem.MongoDBAggregation
            A MongoDB-based shleem data tap.
        identifier : str, optional
            A string identifier for this dataset, preferrably containing only
            lowercase letters, numbers and underscores.
        versioning_scheme : str or function, optional
            If a callable is given, it is assumed to be a valid versioning scheme
            function (see the documenation of the versioning sub-module for
            details). Otherwise, a versioning scheme name is assumed to be given,
            and a versioning scheme is fetched by name. If a bad name or None is
            given, the default versioning scheme is used.
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
            dingle=self.dingle,
            datatap=datatap,
            identifier=identifier,
            versioning_scheme=versioning_scheme,
            fieldnames=fieldnames,
            flatten=flatten,
            missing_val=missing_val,
        )
