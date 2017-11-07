"""Testing core functionalities of the dinglebop package."""

from dinglebop import (
    DataSource,
    DataTap,
)


def test_data_source():
    some_id = "232"
    some_source = DataSource(identifier=some_id)
    assert some_source.identifier == some_id
    assert some_source.source_type == 'unspecified'
    assert some_source.__repr__() == 'DataSource: {}'.format(some_id)

    some_type = "dinglebopDB"
    source2 = DataSource(identifier=some_id, source_type=some_type)
    assert source2.identifier == some_id
    assert source2.source_type == some_type


def test_data_tap():
    class dinglebopDBQuery(DataTap):
        def __init__(self, query):
            super().__init__(
                identifier="dinglebopDB."+str(query), source_type="dinglebopDB")
            self.query = query
        def tap(self):
            return []
    shuq = dinglebopDBQuery({'a': 4})
    assert shuq.source_type == "dinglebopDB"
    assert shuq.__repr__() == "DataTap: dinglebopDB.{'a': 4}"
    assert shuq.tap() == []
