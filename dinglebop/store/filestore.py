"""A file-based dinglebop dataset store."""

import abc

from .store import DingleStore


class FileStore(DingleStore, metaclass=abc.ABCMeta):
    pass
