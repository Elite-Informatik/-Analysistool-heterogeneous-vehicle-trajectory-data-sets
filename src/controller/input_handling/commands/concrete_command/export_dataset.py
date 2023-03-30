from src.controller.execution_handling.export_manager import IExportManager
from src.controller.input_handling.commands.command import Command


class ExportDatasetCommand(Command):
    """represents a command to export the current dataset"""

    def __init__(self, export_manager: IExportManager,
                 path: str, file_format: str):
        """
        creates a new ExportDatasetCommand
        :param export_manager:  the export manager
        :param path:            the path
        :param file_format:     the file format
        """
        super().__init__()
        self._export_manager = export_manager
        self._path = path
        self._format = file_format

    def execute(self):
        """
        exports the dataset
        """
        self._was_successful = self._export_manager.export_dataset(self._path, self._format)
