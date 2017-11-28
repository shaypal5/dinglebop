"""Core functions for the dinglebop package."""

import os
import abc
import glob
import uuid
import functools

from ..shared import (
    CACHE_DIR_PATH,
)
from .versioning import scheme_by_name


DEFAULT_SOURCE_TYPE = 'unspecified'


class Dataset(object, metaclass=abc.ABCMeta):
    """A base class for dinglebop datasets.

    Parameters
    ---------
    dingle : dinglebop.Dingle
        The dingle this dataset will be stored and versioned on.
    identifier : str
        A string identifier unique to this dataset.
    versioning_scheme : str or function, optional
        If a callable is given, it is assumed to be a valid versioning scheme
        function (see the documenation of the versioning sub-module for
        details). Otherwise, a versioning scheme name is assumed to be given,
        and a versioning scheme is fetched by name. If a bad name or None is
        given, the default versioning scheme is used.
    """

    def __init__(self, dingle, identifier, versioning_scheme=None):
        self.dingle = dingle
        self.identifier = identifier
        if callable(versioning_scheme):
            self.versioning_scheme = versioning_scheme
        else:
            self.versioning_scheme = scheme_by_name(versioning_scheme)

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
    def _instantiate(self, version):
        """Instantiate an instance object of this dataset.

        Parameters
        ----------
        version : str
            The version string of the instance.

        Return
        ------
        DatasetInstance
            A dataset instance object.
        """
        pass

    @functools.lru_cache(maxsize=None)
    def _version_cache(self, version):
        return self._instantiate(version=version)

    def version(self, version=None):
        """Returns an instance of this dataset by version.

        Parameters
        ---------
        version : str, optional
            The version string of the instance to get. If such a version is not
            found, a fresh instance with the given version string is returned.
            If no version string is given, a version-less fresh instance, whose
            version string is determined by this dataset's versioning scheme
            upon upload, is returned.
        """
        if version:
            return self._version_cache(version=version)
        return self._instantiate(version=version)

    @abc.abstractclassmethod
    def _file_ext():
        pass

    def _fname(self, version=None):
        """Returns a filename appropriate for a dump of this dataset.

        Parameters
        ---------
        version : str
            The version string to embed in the file name. If None is given, a
            random version string is generated.
        """
        if version is None:
            version = uuid.uuid4().hex
        return self.identifier + '_' + version + '.' + self._file_ext()

    def _get_version_str(self, filepath, dump_dtime, dingle_index):
        """Calculates a version for a specific dump of the dataset.

        Parameters
        ---------
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
        return None

    def dump(self, version=None, filepath=None):
        """Dumps a fresh version of this dataset to a file.

        Parameters
        --------
        version : str
            A version string to append to the default file name schema. If not
            given, a version is inferred. This parameter is ignored if
            filepath is given.
        filepath : str, optional
            The full path to the file into which the dataset will be dumped.
            If not given, the default file naming schema of this dataset type
            is used, and the dump file is created in dinglebop's cache folder.

        Returns
        -------
        str
            The full path of the file into which the dataset was dumped.
        """
        instance = self.version(version=version)
        return instance.dump(filepath=filepath)

    def upload(self, version=None, overwrite=None, ignore_cache=None):
        """Uploads an instance of a dataset with the given version string.

        Parameters
        ---------
        version : str, optional
            The version string of the new version to upload. If not given,
            a new version is inferred using the dataset's versioning scheme and
            given existing versions in the index.
        overwrite : bool, optional
            If set to True, an existing entry with the same version string on
            this dingle will be ignored, if it exists. False by default.
        ignore_cache : bool, optional
            If set to True, an existing dump with the same version string in
            local machine cache will be ignored, if it exists. False by
            default.
        """
        instance = self.version(version=version)
        instance.upload(overwrite=overwrite, ignore_cache=ignore_cache)


class DatasetInstance(object, metaclass=abc.ABCMeta):
    """An instance of a versioned dataset.

    Parameters
    ---------
    dataset : dinglebop.Dataset
        The dataset this instance is a version of.
    version : str
        The version string of this instance.
    """

    def __init__(self, dataset, version):
        self.dataset = dataset
        self.version = version

    @abc.abstractmethod
    def properties(self):
        """Returns a mapping of properties of this dataset instance.

        Returns
        -------
        properties : dict
            A mapping of property names to values.
        """
        pass

    def upload(self, overwrite=None, ignore_cache=None):
        """Uploads this dataset instance.

        Parameters
        ---------
        overwrite : bool, optional
            If set to True, an existing entry with the same version string on
            this dingle will be ignored, if it exists. False by default.
        ignore_cache : bool, optional
            If set to True, an existing dump with the same version string in
            local machine cache will be ignored, if it exists. False by
            default.
        """
        self.dataset.dingle.upload(
            dataset_instance=self,
            overwrite=overwrite,
            ignore_cache=ignore_cache,
        )

    def _dump_fpath(self, filepath=None, version=None):
        if filepath:
            return filepath
        return os.path.join(CACHE_DIR_PATH, self._fname(version=version))

    @abc.abstractmethod
    def _dump_helper(self, filepath):
        pass
