from abc import ABC
from abc import abstractmethod

from src.controller.execution_handling.abstract_manager import AbstractManager
from src.controller.facade_consumer import DataFacadeConsumer
from src.controller.facade_consumer import DatasetFacadeConsumer
from src.controller.facade_consumer.file_facade_consumer import FileFacadeConsumer
from src.controller.output_handling.event import (DatasetExported)
from src.data_transfer.content import Column
from src.data_transfer.content import type_check
from src.data_transfer.record import DataRecord
from src.data_transfer.record import FileRecord

STANDARD_DATA_FORMAT: str = 'csv'
EXPORT_MSG: str = "Dataset exported successful"


class IExportManager(ABC):
    """
    This Manager Interface can be used to export datasets and files.
    """

    @abstractmethod
    def export_dataset(self, path, file_format: str) -> bool:
        """
        exports a dataset with a given UUID to a given path
        :return:    True if the export was successful, False otherwise
        """
        pass

    @abstractmethod
    def export_file(self, file: FileRecord, path: str) -> bool:
        """
        exports a given file to a given path
        """
        pass


class ExportManager(AbstractManager, DataFacadeConsumer, IExportManager, DatasetFacadeConsumer, FileFacadeConsumer):
    """
    The ExportManager implements the ExportManager Interface. It makes use of the FileFacade and DataFacade to structure
    the file flow in between them.
    """

    @type_check(str, str)
    def export_dataset(self, path: str, file_format: str) -> bool:
        dataset: DataRecord = self._data_facade.get_data(Column.list())

        if self.file_facade.export_data_file(path, dataset, file_format):
            self.events.append(DatasetExported())
            self.request_manager.send_messages([EXPORT_MSG])
            return True

        self.handle_error([self.file_facade])
        return False

    @type_check(FileRecord, str)
    def export_file(self, file: FileRecord, path: str) -> bool:
        if not self.file_facade.export_file(path, file):
            self.handle_error([self.file_facade])
            return False
        return True
