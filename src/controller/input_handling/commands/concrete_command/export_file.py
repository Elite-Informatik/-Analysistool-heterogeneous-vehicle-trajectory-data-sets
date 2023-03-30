from src.controller.execution_handling.export_manager import IExportManager
from src.controller.input_handling.commands.command import Command
from src.data_transfer.record import FileRecord


class ExportFileCommand(Command):
    """
    represents a command to export a file
    """

    def __init__(self, export_manager: IExportManager, file: FileRecord, path: str):
        """
        creates a new ExportFileCommand
        :param file:            the file to export
        :param path:            the path
        :param export_manager:    the export manager
        """
        super().__init__()
        self._file = file
        self._path = path
        self._export_manager = export_manager

    def execute(self):
        """
        exports the file to the given path
        """
        self._was_successful = self._export_manager.export_file(self._file, self._path)
