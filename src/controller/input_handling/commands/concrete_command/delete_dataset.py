from uuid import UUID

from src.controller.execution_handling.database_manager import IDatabaseManager
from src.controller.input_handling.commands.command import Command


class DeleteDatasetCommand(Command):
    """
    represents a command to delete a dataset
    """

    def __init__(self, uuid: UUID, dataset_manager: IDatabaseManager):
        """
        creates a new DeleteDatasetCommand
        :param uuid:            the id of the dataset to delete
        :param dataset_manager: the dataset manager
        """
        super().__init__()
        self._dataset_id = uuid
        self._dataset_manager = dataset_manager

    def execute(self):
        """
        deletes the dataset with the given id
        """
        self._was_successful = self._dataset_manager.delete_dataset(self._dataset_id)
