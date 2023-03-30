from src.controller.execution_handling.analysis_manager import IAnalysisManager
from src.controller.input_handling.commands.command import Command


class ImportAnalysisCommand(Command):
    """
    represents a Command to import a new analysis
    """

    def __init__(self, analysis_manager: IAnalysisManager, path: str):
        """
        creates a new ImportAnalysisCommand
        :param analysis_manager:    the analysis manager
        :param path:                the path of the new analysis
        """
        super().__init__()
        self._analysis_manager = analysis_manager
        self._path = path

    def execute(self):
        """
        imports the new analysis
        """
        self._was_successful = self._analysis_manager.import_analysis(self._path)
