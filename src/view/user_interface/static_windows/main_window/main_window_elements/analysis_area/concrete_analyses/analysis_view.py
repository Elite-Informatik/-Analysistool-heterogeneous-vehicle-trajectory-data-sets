import tkinter as tk
from abc import ABC
from abc import abstractmethod
from typing import List
from uuid import UUID

from pandas import DataFrame

from src.data_transfer.record import AnalysisDataRecord
from src.data_transfer.record import DataRecord
from src.data_transfer.record import FileRecord


class AnalysisView(ABC):
    """
    This abstract class represents a visualisation of an analysis
    """

    def __init__(self, analysed_data: DataRecord, analysis_id: UUID, name: str = "New Analysis"):
        """
        creates a new analysis view
        :param analysed_data:   the analysed data of the analysis
        :param analysis_id:     the id of the analysis to display
        """
        self._analysed_data: DataRecord = analysed_data
        self._id: UUID = analysis_id
        self._view_frame: tk.Frame = None
        self._view_widget: tk.Widget = None
        self._name: str = name

    def build(self, master: tk.Frame) -> tk.Widget:
        """
        builds the analysis view
        :param master:  the master
        :return:        the Widget containing the analysis view
        """
        data_frame = self._analysed_data.data
        self._view_frame = tk.Frame(master)
        self._view_widget = self._create_figure(self._view_frame, data_frame)
        self._view_widget.pack(fill="both", expand=True)
        return self._view_frame

    @abstractmethod
    def _create_figure(self, master, data_frame: DataFrame) -> tk.Widget:
        pass

    @abstractmethod
    def export(self, format: str, file_name: str) -> FileRecord:
        """
        exports itself into the given format
        :param format:      the data format
        :param file_name:   the _name of the file
        :return:            the file to export
        """
        pass

    def refresh(self, analyzed_data: AnalysisDataRecord):
        """
        refreshes the analysis view: updates the displayed data
        :param analyzed_data:   the new analyzed data
        """
        self._analysed_data = analyzed_data.data
        self._view_widget.destroy()
        self._view_widget = self._create_figure(self._view_frame, analyzed_data.data.data)
        self._view_widget.pack(fill="both", expand=True)

    @abstractmethod
    def get_available_export_formats(self) -> List[str]:
        """
        gets all export formats in which this analysis view can be exported
        :return:  the available export formats
        """
        pass

    def get_name(self) -> str:
        """
        gets the name of the analysis view
        :return:    the name of the analysis view
        """
        return self._name
