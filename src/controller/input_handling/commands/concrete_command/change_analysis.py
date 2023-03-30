from typing import Optional
from uuid import UUID

from src.controller.execution_handling.analysis_manager import IAnalysisGetter
from src.controller.execution_handling.analysis_manager import IAnalysisManager
from src.controller.input_handling.commands.undoable import Undoable
from src.data_transfer.record import AnalysisRecord


class ChangeAnalysisCommand(Undoable):
    """
    represents a command to change an analysis
    """

    def __init__(self, analysis_manager: IAnalysisManager, analysis_getter: IAnalysisGetter, analysis_id: UUID,
                 analysis_setting: AnalysisRecord):
        """
        creates a new ChangeAnalysisCommand
        :param analysis_manager:    the analysis manager
        :param analysis_id:         the id of the analysis to change
        :param analysis_setting:    the new parameters of the analysis
        """
        super().__init__()
        self._analysis_manager = analysis_manager
        self._analysis_getter = analysis_getter
        self._analysis_id = analysis_id
        self._new_analysis_setting = analysis_setting
        self._old_analysis: Optional[AnalysisRecord] = None

    def undo(self):
        """
        undoes itself: restores the old settings of the changed analysis
        """
        if self._old_analysis is not None:
            self._analysis_manager.edit_analysis_settings(self._analysis_id, self._old_analysis)

    def execute(self):
        """
        changes the analysis
        """
        self._old_analysis = self._analysis_getter.get_analysis_settings(self._analysis_id)
        self._was_successful = self._analysis_manager.edit_analysis_settings(self._analysis_id,
                                                                             self._new_analysis_setting)
