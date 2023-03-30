import tkinter as tk
from typing import List
from uuid import UUID

from matplotlib.figure import Figure
from pandas import DataFrame

from src.data_transfer.content import Column
from src.data_transfer.record import DataRecord
from src.data_transfer.record import FileRecord
from src.data_transfer.record.file_record_csv import FileRecordCsv
from src.data_transfer.record.file_record_png import FileRecordPng
from src.data_transfer.record.file_record_svg import FileRecordSvg
from src.view.user_interface.static_windows.main_window.main_window_elements.analysis_area import analysis_util
from src.view.user_interface.static_windows.main_window.main_window_elements.analysis_area.concrete_analyses.analysis_view import \
    AnalysisView
from src.view.user_interface.static_windows.main_window.main_window_elements.analysis_area.export_formats import \
    AnalysisExportFormatEnum


class BarcodeAnalysisView(AnalysisView):
    """
    represents a plot with connected points
    """

    ANALYSIS_VIEW_ID: int = 4
    _PLOT_COLOR = 'r'

    def __init__(self, analysed_data: DataRecord, analysis_id: UUID, name: str = "Barcode"):
        """
        Constructor for a new barcode analysis view
        """
        super().__init__(analysed_data, analysis_id, name)

    def _create_figure(self, master, data_frame: DataFrame) -> tk.Widget:
        """
        Creates the barcode based on the given dataframe
        :param master: the masterframe of the analysis
        :param data_frame: the data content
        """
        x_name = data_frame.columns[1]
        y_name = data_frame.columns[2]

        figure_canvas = analysis_util.prepare_analysis_figure(master, x_name, y_name)
        self._figure: Figure = figure_canvas.figure
        ax = self._figure.get_axes()[0]

        data_frame = analysis_util.prepare_dataformats(data_frame);

        for name, group in data_frame.groupby(Column.TRAJECTORY_ID.value):
            ax.plot(group[x_name], group[y_name], color=self._PLOT_COLOR)

        analysis_util.optimize_axes_labels(ax)

        return figure_canvas.get_tk_widget()

    def export(self, format: str, file_name: str) -> FileRecord:
        """
        Exports the data
        :param format: the format of the export
        :param file_name: the file_name of the file
        """
        if format == AnalysisExportFormatEnum.CSV.value:
            return FileRecordCsv(self._analysed_data.data, file_name)
        elif format == AnalysisExportFormatEnum.SVG.value:
            return FileRecordSvg(self._figure, file_name)
        elif format == AnalysisExportFormatEnum.PNG.value:
            return FileRecordPng(self._figure, file_name)
        return None

    def get_available_export_formats(self) -> List[str]:
        """
        Returns all exportable format
        :return: List of all strings
        """
        return [AnalysisExportFormatEnum.CSV.value, AnalysisExportFormatEnum.PNG.value,
                AnalysisExportFormatEnum.SVG.value]
