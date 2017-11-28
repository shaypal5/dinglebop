"""MongoDB-related utilities used by the dinglebop package."""

import csv

from strct.dicts import flatten_dict
from bson.json_util import (
    dumps,
    loads,
)


def dump_document_cursor_to_json(doc_cursor, file_path):
    """Writes documents in a pymongo cursor into a json file.

    Parameters
    ---------
    doc_cursor : pymongo.cursor.Cursor
        A pymongo document cursor returned by commands like find or aggregate.
    file_path : str
        The full path of the file into which cursor documents are dumped.
    """
    with open(file_path, 'w+') as dump_json:
        dump_json.write('[\n')
        dump_json.write(dumps(doc_cursor.next()))
        for doc in doc_cursor:
            dump_json.write(',\n')
            dump_json.write(dumps(doc))
        dump_json.write('\n]')


def load_document_iterator_from_json(file_path):
    """Creates a lazy iterator over documents from a json file.

    Parameters
    ---------
    file_path : str
        The full path of the file from which documents are read.
    """
    with open(file_path, 'r') as load_json:
        line = load_json.readline()
        while line:
            if line not in ('[\n', ']'):  # ignore start and end of array
                try:  # skip trailing , and one \n
                    yield loads(line[:-2])
                except JSONDecodeError:  # last line has no , so just \n
                    yield loads(line[:-1])
            line = load_json.readline()
        raise StopIteration
