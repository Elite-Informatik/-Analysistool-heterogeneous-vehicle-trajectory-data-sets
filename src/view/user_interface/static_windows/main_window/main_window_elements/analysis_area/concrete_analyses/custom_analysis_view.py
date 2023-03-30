import tkinter as tk
from typing import List
from uuid import UUID

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from pandas import DataFrame

from src.data_transfer.record import AnalysisDataRecord
from src.data_transfer.record import DataRecord
from src.data_transfer.record import FileRecord
from src.data_transfer.record.file_record_csv import FileRecordCsv
from src.data_transfer.record.file_record_png import FileRecordPng
from src.data_transfer.record.file_record_svg import FileRecordSvg
from src.view.user_interface.static_windows.main_window.main_window_elements.analysis_area.concrete_analyses.analysis_view import \
    AnalysisView
from src.view.user_interface.static_windows.main_window.main_window_elements.analysis_area.export_formats import \
    AnalysisExportFormatEnum


class CustomAnalysisView(AnalysisView):
    """
    This analysis view represents a custom analysis view:
    It gives users the chance to define their analysis view in the imported analysis scripts.
    """

    def __init__(self, analysed_data: DataRecord, analysis_id: UUID, figure: Figure, name: str = "Custom"):
        super().__init__(analysed_data, analysis_id, name)
        self._figure = figure

    def _create_figure(self, master, data_frame: DataFrame) -> tk.Widget:
        figure_canvas = FigureCanvasTkAgg(self._figure, master)
        return figure_canvas.get_tk_widget()

    def export(self, format: str, file_name: str) -> FileRecord:
        if format == AnalysisExportFormatEnum.CSV.value:
            return FileRecordCsv(self._analysed_data.data, file_name)
        elif format == AnalysisExportFormatEnum.SVG.value:
            return FileRecordSvg(self._figure, file_name)
        elif format == AnalysisExportFormatEnum.PNG.value:
            return FileRecordPng(self._figure, file_name)
        return None

    def refresh(self, analyzed_data: AnalysisDataRecord):
        self._figure = analyzed_data.plot
        super().refresh(analyzed_data)

    def get_available_export_formats(self) -> List[str]:
        return [AnalysisExportFormatEnum.CSV.value, AnalysisExportFormatEnum.PNG.value,
                AnalysisExportFormatEnum.SVG.value]
