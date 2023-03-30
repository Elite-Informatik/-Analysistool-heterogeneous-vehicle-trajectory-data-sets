from typing import Optional

from matplotlib.figure import Figure

from src.data_transfer.content.analysis_view import AnalysisViewEnum
from src.data_transfer.record.data_record import DataRecord


class AnalysisDataRecord:
    """
    record that holds the analysed data and the analysis view type to display it
    """

    def __init__(self, _data: Optional[DataRecord] = None, _view_id: Optional[AnalysisViewEnum] = None,
                 _plot: Optional[Figure] = None):
        """
        creates a new AnalysisDataRecord. Either data and view id or plot must be given.
        :param _data: Optional[DataRecord] the analysed data. If None, plot must be given.
        :param _view_id: Optional[AnalysisViewEnum] the analysis view id. If None, plot must be given.
        :param _plot: Optional[Figure] the plot to display. If None, data and view id must be given.
        """
        if (_plot is None and _data is None) or (_plot is None and _view_id is None):
            raise ValueError("Either data and view id or plot must be given")
        self._data = _data
        self._view_id = _view_id
        self._plot = _plot

    @property
    def data(self):
        """
        the analysed data
        """
        return self._data

    @property
    def id(self):
        """
        the analysis view id
        """
        return self._view_id

    @property
    def plot(self):
        """
        the plot to display
        """
        return self._plot
