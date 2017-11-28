"""An Azure blob based dinglebop dataset store."""

from decore import lazy_property
from azure.storage.blob import BlockBlobService

from .store import DingleStore


class AzureBlobStore(DingleStore):
    """An Azure Blob-based implmentation of DingleStore.

    Parameters
    ---------
    account_name : str
        The name of the Azure account the Blob container belongs to.
    account_key : str
        The key of the Azure account the Blob container belongs to.
    container_name : str
        The name of this Blob container.
    """

    def __init__(self, name, account_name, account_key, container_name):
        super().__init__(name=name)
        self.account_name = account_name
        self.account_key = account_key
        self.container_name = container_name

    @lazy_property
    def _blob_service(self):
        bserv = BlockBlobService(account_name=self.account_name,
                                 account_key=self.account_key)
        if not bserv.exists(self.container_name):
            bserv.create_container(self.container_name)
        return bserv

    @staticmethod
    def _blob_name(dataset, version):
        return dataset.identifier + '.' + version

    def upload(self, dataset, version):
        blob_name = self._blob_name(dataset, version)
        bserv = self._blob_service()
        fpath = dataset.dump(version=version)
        bserv.create_blob_from_path(
            container_name=self.container_name,
            blob_name=blob_name,
            file_path=fpath,
        )

    def download(self, dataset, version, filepath):
        pass

    def delete(self, dataset, version):
        pass
