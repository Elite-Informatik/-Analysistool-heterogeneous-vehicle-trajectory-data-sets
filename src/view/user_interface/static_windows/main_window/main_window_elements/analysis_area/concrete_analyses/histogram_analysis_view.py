import tkinter as tk
from typing import List
from typing import Optional
from uuid import UUID

from matplotlib.figure import Figure
from pandas import DataFrame

from src.data_transfer.record import DataRecord
from src.data_transfer.record import FileRecord
from src.data_transfer.record.file_record_csv import FileRecordCsv
from src.data_transfer.record.file_record_png import FileRecordPng
from src.data_transfer.record.file_record_svg import FileRecordSvg
from src.view.user_interface.static_windows.main_window.main_window_elements.analysis_area import analysis_util
from src.view.user_interface.static_windows.main_window.main_window_elements.analysis_area.concrete_analyses \
    .analysis_view import \
    AnalysisView
from src.view.user_interface.static_windows.main_window.main_window_elements.analysis_area.export_formats import \
    AnalysisExportFormatEnum


class HistogramAnalysisView(AnalysisView):
    """
    This analysis view displays analysed data in form of a histogram
    """

    ANALYSIS_VIEW_ID: int = 0
    _BAR_COLOR = 'r'

    def __init__(self, analysed_data: DataRecord, analysis_id: UUID, name: str = 'Histogram'):
        super().__init__(analysed_data, analysis_id, name)

    def _create_figure(self, master, data_frame: DataFrame) -> tk.Widget:
        x_name = data_frame.columns[0]
        y_name = data_frame.columns[1]
        # data_frame[x_name] = analysis_util.prepare_columnformat(data_frame[x_name])
        # data_frame[y_name] = analysis_util.prepare_columnformat(data_frame[y_name])
        print(data_frame[x_name][0])
        figure_canvas = analysis_util.prepare_analysis_figure(master, x_name, y_name)
        self._figure: Figure = figure_canvas.figure
        ax = self._figure.get_axes()[0]

        ax.bar(data_frame[x_name], data_frame[y_name], color=self._BAR_COLOR)
        analysis_util.optimize_axes_labels(ax)
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
        return [AnalysisExportFormatEnum.CSV.value, AnalysisExportFormatEnum.PNG.value,
                AnalysisExportFormatEnum.SVG.value]

    @property
    def id(self) -> UUID:
        return self._id
