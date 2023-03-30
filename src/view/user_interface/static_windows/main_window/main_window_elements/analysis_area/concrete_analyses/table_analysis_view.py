import tkinter as tk
from typing import List
from typing import Optional
from uuid import UUID

from pandas import DataFrame
from pandastable import Table

from src.data_transfer.record import DataRecord
from src.data_transfer.record import FileRecord
from src.data_transfer.record.file_record_csv import FileRecordCsv
from src.view.user_interface.static_windows.main_window.main_window_elements.analysis_area.concrete_analyses \
    .analysis_view import \
    AnalysisView
from src.view.user_interface.static_windows.main_window.main_window_elements.analysis_area.export_formats import \
    AnalysisExportFormatEnum


class TableAnalysisView(AnalysisView):
    """
    This analysis view displays analysed data in form of a table
    """

    ANALYSIS_VIEW_ID: int = 1

    def __init__(self, analysed_data: DataRecord, analysis_id: UUID, name: str = "Table"):
        super().__init__(analysed_data, analysis_id, name)

    def _create_figure(self, master, data_frame: DataFrame) -> tk.Widget:
        table_frame = tk.Frame(master)
        table = Table(table_frame, dataframe=data_frame, editable=False)
        table.show()
        return table_frame

    def export(self, format: str, file_name: str) -> Optional[FileRecord]:
        if format == AnalysisExportFormatEnum.CSV.value:
            return FileRecordCsv(self._analysed_data.data, file_name)
        return None

    def get_available_export_formats(self) -> List[str]:
        return [AnalysisExportFormatEnum.CSV.value]

    @property
    def id(self) -> UUID:
        return self._id
