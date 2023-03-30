from uuid import UUID

from src.controller.execution_handling.database_manager import IDatabaseManager
from src.controller.input_handling.commands.command import Command


class OpenDatasetCommand(Command):
    """represents a command to open a dataset"""

    def __init__(self, dataset_id: UUID, database_manager: IDatabaseManager):
        """
        creates a new OpenDatasetCommand
        :param dataset_id:          the id of the dataset to open
        :param database_manager:    the database manager
        """
        super().__init__()
        self._database_manager: IDatabaseManager = database_manager
        self._dataset_id = dataset_id

    def execute(self):
        """
        opens the dataset
        """
        self._was_successful = self._database_manager.open_dataset(self._dataset_id)
