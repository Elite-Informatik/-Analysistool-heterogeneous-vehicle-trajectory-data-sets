from typing import List
from typing import Optional
from uuid import UUID

from src.controller.execution_handling.database_manager import IDatabaseManager
from src.controller.input_handling.commands.undoable import Undoable


class ImportDatasetCommand(Undoable):
    """represents a command to import a new dataset"""

    def __init__(self,
                 dataset_manager: IDatabaseManager,
                 paths: List[str],
                 name: str,
                 file_format: str):
        """
        creates a new ImportDatasetCommand
        :param dataset_manager:  the dataset manager
        :param paths:            the paths of the files for dataset
        :param file_format:      the file format
        """
        super().__init__()
        self._dataset_id: Optional[UUID] = None
        self._paths = paths
        self._name = name
        self._format = file_format
        self._dataset_manager = dataset_manager

    def undo(self):
        """
        undoes itself: deletes the imported dataset
        """
        self._dataset_manager.delete_dataset(self._dataset_id)

    def execute(self):
        """
        imports the new dataset
        """
        self._was_successful = self._dataset_manager.import_dataset(self._paths, self._name, self._format)
