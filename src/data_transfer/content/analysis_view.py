from enum import Enum


class AnalysisViewEnum(Enum):
    """
    holds all available analysis view types
    """

    histogram_view = "histogram view"
    plot_view = "plot view"
    table_view = "table view"
    heatmap_view = "heatmap view"
    bar_code_view = "bar code"
