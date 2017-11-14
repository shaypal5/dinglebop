"""Testing the implementation of MongoDB-based dingle indexes."""

import pytest

from dinglebop.index.mongodb import MongoDBIndex
from dinglebop.shared import get_dinglebop_cfg


SAMPLE_IDEN1 = 'school_data_2016'
SAMPLE_IDEN2 = 'school_data_2017'
SAMPLE_DOC1 = {'identifier': SAMPLE_IDEN1, 'version': 'v1.0',
               'store': 'somestore', 'format_identifier': 'arrow'}
SAMPLE_DOC2 = {'identifier': SAMPLE_IDEN1, 'version': 'v1.1',
               'store': 'somestore', 'format_identifier': 'csv'}
SAMPLE_DOC3 = {'identifier': SAMPLE_IDEN2, 'version': 'v0.03',
               'store': 'somestore', 'format_identifier': 'csv'}
SAMPLE_DOC4 = {'identifier': SAMPLE_IDEN2, 'version': 'v0.23',
               'store': 'somestore', 'format_identifier': 'csv'}
SAMPLE_DOCS = [SAMPLE_DOC1, SAMPLE_DOC2, SAMPLE_DOC3, SAMPLE_DOC4]


def _get_mongodb_idx_instance():
    dcfg = get_dinglebop_cfg()
    idx_cfg = dcfg['dingles']['dinglebop_test']['index'].copy()
    assert idx_cfg.pop('type') == 'MongoDB'
    return MongoDBIndex(**idx_cfg)


def _get_idx_collection():
    return _get_mongodb_idx_instance()._get_collection()


@pytest.fixture(scope="session", autouse=True)
def reset_idx_collection():
    idx_obj = _get_mongodb_idx_instance()
    collection = idx_obj._get_collection()
    if MongoDBIndex._INDEX_NAME in collection.index_information():
        collection.drop_index(MongoDBIndex._INDEX_NAME)
    collection.delete_many({})
    collection.insert_many([d.copy() for d in SAMPLE_DOCS])


def test_mongodb_index_autocreation():
    idx_collection = _get_idx_collection()
    assert MongoDBIndex._INDEX_NAME in idx_collection.index_information()


def test_get_all_dataset_entries():
    dingle_idx = _get_mongodb_idx_instance()
    cursor = dingle_idx.get_all_dataset_entries(identifier=SAMPLE_IDEN1)
    docs = list(cursor)
    assert len(docs) == 2
    assert docs[0]['version'] == 'v1.1'
    assert docs[1]['version'] == 'v1.0'


def test_get_latest_dataset_entry():
    dingle_idx = _get_mongodb_idx_instance()
    doc1 = dingle_idx.get_latest_dataset_entry(identifier=SAMPLE_IDEN1)
    assert doc1['version'] == 'v1.1'
    doc2 = dingle_idx.get_latest_dataset_entry(identifier=SAMPLE_IDEN2)
    assert doc2['version'] == 'v0.23'


def test_get_dataset_entry_by_version():
    dingle_idx = _get_mongodb_idx_instance()
    doc = dingle_idx.get_dataset_entry_by_version(
        identifier=SAMPLE_IDEN1, version='v1.0')
    assert doc['format_identifier'] == 'arrow'


@pytest.fixture(scope='function')
def clear_all_idx_docs():
    collection = _get_idx_collection()
    collection.delete_many({})


def test_add_entry(clear_all_idx_docs):
    dingle_idx = _get_mongodb_idx_instance()
    dingle_idx.add_entry(**SAMPLE_DOC1)
    dingle_idx.add_entry(**SAMPLE_DOC2)
    docs = list(dingle_idx.get_all_dataset_entries(identifier=SAMPLE_IDEN1))
    assert len(docs) == 2


@pytest.fixture(scope='function')
def add_all_idx_docs():
    collection = _get_idx_collection()
    collection.delete_many({})
    collection.insert_many([d.copy() for d in SAMPLE_DOCS])


def test_remove_entries(add_all_idx_docs):
    dingle_idx = _get_mongodb_idx_instance()
    docs1 = list(dingle_idx.get_all_dataset_entries(identifier=SAMPLE_IDEN1))
    assert len(docs1) == 2
    docs2 = list(dingle_idx.get_all_dataset_entries(identifier=SAMPLE_IDEN2))
    assert len(docs2) == 2

    dingle_idx.remove_entries(identifier=SAMPLE_IDEN1, version='v1.0')
    docs1 = list(dingle_idx.get_all_dataset_entries(identifier=SAMPLE_IDEN1))
    assert len(docs1) == 1

    dingle_idx.remove_entries(identifier=SAMPLE_IDEN2)
    docs2 = list(dingle_idx.get_all_dataset_entries(identifier=SAMPLE_IDEN2))
    assert len(docs2) == 0
