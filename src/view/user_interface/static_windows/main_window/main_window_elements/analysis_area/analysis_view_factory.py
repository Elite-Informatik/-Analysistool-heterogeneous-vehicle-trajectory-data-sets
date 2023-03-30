import uuid
from typing import Optional

from src.data_transfer.content.analysis_view import AnalysisViewEnum
from src.data_transfer.record import AnalysisDataRecord
from src.view.user_interface.static_windows.main_window.main_window_elements.analysis_area.concrete_analyses \
    .analysis_view import AnalysisView
from src.view.user_interface.static_windows.main_window.main_window_elements.analysis_area.concrete_analyses.barcode_analysis_view import \
    BarcodeAnalysisView
from src.view.user_interface.static_windows.main_window.main_window_elements.analysis_area.concrete_analyses.custom_analysis_view import \
    CustomAnalysisView
from src.view.user_interface.static_windows.main_window.main_window_elements.analysis_area.concrete_analyses \
    .heatmap_analysis_view import HeatmapAnalysisView
from src.view.user_interface.static_windows.main_window.main_window_elements.analysis_area.concrete_analyses \
    .histogram_analysis_view import HistogramAnalysisView
from src.view.user_interface.static_windows.main_window.main_window_elements.analysis_area.concrete_analyses \
    .plot_analysis_view import PlotAnalysisView
from src.view.user_interface.static_windows.main_window.main_window_elements.analysis_area.concrete_analyses \
    .table_analysis_view import TableAnalysisView


class AnalysisViewFactory:
    """
    represents a factory to create analysis views
    """

    def create_analysis_view(self, data: AnalysisDataRecord, analysis_id: uuid.UUID) -> Optional[AnalysisView]:
        """
        creates a new analysis view out of the given analysis data record
        :param analysis_id:     the id of the new analysis
        :param data:            the analysis data record
        :return:                the new analysis view
        """
        analysis_type = data.id
        analyzed_data = data.data
        if data.plot is not None:
            return CustomAnalysisView(analyzed_data, analysis_id, data.plot, data.data.name)
        if analysis_type == AnalysisViewEnum.plot_view:
            return PlotAnalysisView(analyzed_data, analysis_id, data.data.name)
        if analysis_type == AnalysisViewEnum.table_view:
            return TableAnalysisView(analyzed_data, analysis_id, data.data.name)
        if analysis_type == AnalysisViewEnum.heatmap_view:
            return HeatmapAnalysisView(analyzed_data, analysis_id, data.data.name)
        if analysis_type == AnalysisViewEnum.histogram_view:
            return HistogramAnalysisView(analyzed_data, analysis_id, data.data.name)
        if analysis_type == AnalysisViewEnum.bar_code_view:
            return BarcodeAnalysisView(analyzed_data, analysis_id, data.data.name)
        return None
