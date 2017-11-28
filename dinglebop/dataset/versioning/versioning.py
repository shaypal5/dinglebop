"""Versioning schemes for datasets.

Versioning scheme are functions that calculate a version for a specific dump
of a dataset, and have the following arguments and return type:

Parameters
---------
dataset : dinglebop.DataSet
    A dataset object representing a versioned dataset.
filepath : str
    The full qualified path to the dataset dump.
dump_dtime : datetime.datetime
    A datetime object representing the time the dump was made.
dingle_index : DingleIndex
    An object representing the Dingle index against which this dump
    should be versioned.

Returns
-------
version : str
    A version string.
"""


_NAME_TO_SCHEME = {}


def scheme_by_name(scheme_name=None):
    """Returns a versioning scheme by its name.

    Parameters
    ---------
    scheme_name : str, optional
        The name of the scheme to get. If None is given, the default scheme is
        returned.

    Returns
    -------
    scheme : function
        A versioning scheme function. See module docstring for details.
    """
    try:
        return _NAME_TO_SCHEME[scheme_name]
    except KeyError:
        try:
            return _NAME_TO_SCHEME[None]
        except KeyError:
            return None


def _set_scheme_by_name(scheme_name, scheme):
    """Sets a mapping of a version scheme name to a version scheme function,
    to be used by the scheme_by_name() function.

    Parameters
    ---------
    scheme_name : str
        The scheme name to map. Give None explicitly to set the given scheme
        as the default scheme.
    scheme : function
        A versioning scheme function. See module doctring for details.
    """
    _NAME_TO_SCHEME[scheme_name] = scheme
