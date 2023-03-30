import tkinter as tk
from typing import List
from typing import Optional
from uuid import UUID

import seaborn as sb
from matplotlib.figure import Figure
from pandas import DataFrame

from src.data_transfer.record import DataRecord
from src.data_transfer.record import FileRecord
from src.data_transfer.record.file_record_csv import FileRecordCsv
from src.data_transfer.record.file_record_png import FileRecordPng
from src.data_transfer.record.file_record_svg import FileRecordSvg
from src.view.user_interface.static_windows.main_window.main_window_elements.analysis_area import analysis_util
from src.view.user_interface.static_windows.main_window.main_window_elements.analysis_area.concrete_analyses \
    .analysis_view import AnalysisView
from src.view.user_interface.static_windows.main_window.main_window_elements.analysis_area.export_formats import \
    AnalysisExportFormatEnum


class HeatmapAnalysisView(AnalysisView):
    """
    This AnalysisView displays analysed data in form of a heatmap
    """

    ANALYSIS_VIEW_ID: int = 3
    _HISTOGRAM_COLORMAP = 'Blues_r'
    _INTERPOLATION = 'nearest'

    def __init__(self, analysed_data: DataRecord, analysis_id: UUID, name: str = 'Heatmap'):
        super().__init__(analysed_data, analysis_id, name)

    def _create_figure(self, master, data_frame: DataFrame) -> tk.Widget:
        data_frame = data_frame[::-1]
        figure_canvas = analysis_util.prepare_analysis_figure(master)
        self._figure: Figure = figure_canvas.figure
        ax = self._figure.get_axes()[0]
        sb.heatmap(data_frame, ax=ax)
        return figure_canvas.get_tk_widget()

    def export(self, format: str, file_name: str) -> Optional[FileRecord]:
        if format == AnalysisExportFormatEnum.CSV.value:
            return FileRecordCsv(self._analysed_data.data, file_name)
        elif format == AnalysisExportFormatEnum.SVG.value:
            return FileRecordSvg(self._figure, file_name)
        elif format == AnalysisExportFormatEnum.PNG.value:
            return FileRecordPng(self._figure, file_name)
        return None

    def get_available_export_formats(self) -> List[str]:
        return [AnalysisExportFormatEnum.CSV.value,
                AnalysisExportFormatEnum.PNG.value,
                AnalysisExportFormatEnum.SVG.value]

    @property
    def id(self) -> UUID:
        return self._id
