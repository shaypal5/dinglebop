"""A MongoDB-based implementation of the DingleIndex abstraction."""

import functools
import urllib

from pymongo import (
    MongoClient,
    IndexModel,
    ASCENDING,
    DESCENDING,
)

from .index import DingleIndex


class MongoDBIndex(DingleIndex):
    """A MongoDB-based implmentation of DingleIndex.

    Parameters
    ----------
    hosts : list
        A list of host address string of the form <hostname>:<port>.
    username : str
        A user name used for authentication. The corresponding user must have
        writing permissions for the provided collection.
    password : str
        A password used for authentication.
    db_name : str
        The name of the database which contains the index collection on the
        target server.
    collection_name : str
        The name of the collection which contains the index on the target
        server.

    Any additional keyword arguments are supplied to the constructor of
    pymongo.mongo_client.MongoClient.
    """

    def __init__(self, hosts, username, password, db_name,
                 collection_name, **kwargs):
        self.hosts = hosts
        self.username = username
        self.password = password
        self.db_name = db_name
        self.collection_name = collection_name
        self.extra_kwargs = kwargs
        if 'host' in self.extra_kwargs:
            self.extra_kwargs.pop('host')  # pragma: no cover
        self.uris = MongoDBIndex._mongodb_uris(
            usr=username, pwd=password, hosts=hosts)

    @staticmethod
    def _mongodb_uris(usr, pwd, hosts):
        parsed_usr = urllib.parse.quote_plus(usr)
        parsed_pwd = urllib.parse.quote_plus(pwd)
        return [
            "mongodb://{usr}:{pwd}@{host}".format(
                usr=parsed_usr, pwd=parsed_pwd, host=host)
            for host in hosts
        ]

    _INDEX_NAME = 'identifier_1_version_1'

    @classmethod
    def _init_index_collection(cls, collection_obj):
        index_inf = collection_obj.index_information()
        if cls._INDEX_NAME not in index_inf:
            idx_model = IndexModel(
                keys=[('identifier', ASCENDING), ('version', ASCENDING)],
                name=cls._INDEX_NAME)
            collection_obj.create_indexes([idx_model])

    @functools.lru_cache(maxsize=1)
    def _get_collection(self):
        client = MongoClient(host=self.uris, **self.extra_kwargs)
        collection_obj = client[self.db_name][self.collection_name]
        self._init_index_collection(collection_obj=collection_obj)
        return collection_obj

    def get_all_dataset_entries(self, identifier, descending=True):
        sort_order = DESCENDING if descending else ASCENDING
        return self._get_collection().find(
            filter={'identifier': identifier},
            projection={'_id': 0, 'identifier': 1, 'version': 1,
                        'store': 1, 'format_identifier': 1},
            sort=[('identifier', sort_order), ('version', sort_order)],
        )

    def get_latest_dataset_entry(self, identifier):
        return self._get_collection().find_one(
            filter={'identifier': identifier},
            projection={'_id': 0, 'identifier': 1, 'version': 1,
                        'store': 1, 'format_identifier': 1},
            sort=[('identifier', DESCENDING), ('version', DESCENDING)],
        )

    def get_dataset_entry_by_version(self, identifier, version):
        return self._get_collection().find_one({
            'identifier': identifier, 'version': version})

    def add_entry(self, identifier, version, store, format_identifier):
        self._get_collection().insert_one({
            'identifier': identifier, 'version': version, 'store': store,
            'format_identifier': format_identifier})

    def remove_entries(self, identifier, version=None):
        if version:
            self._get_collection().delete_one({
                'identifier': identifier, 'version': version})
        else:
            self._get_collection().delete_many({'identifier': identifier})
