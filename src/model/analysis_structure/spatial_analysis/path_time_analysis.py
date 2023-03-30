import pandas as pd

from src.data_transfer.content import Column
from src.data_transfer.record import AnalysisDataRecord
from src.data_transfer.record import DataRecord
from src.model.analysis_structure.Analysis import Analysis
from src.model.analysis_structure.spatial_analysis.start_end_analysis import StartEndAnalysis


class PathTimeAnalysis(StartEndAnalysis):
    """
    This class prepares the data for the path time analysis. It prepares to columns to be plotted against each other:
    The time vs the distance taken.
    """

    _columns = [Column.TRAJECTORY_ID.value, Column.DATE.value, Column.TIME.value, Column.LONGITUDE.value,
                Column.LATITUDE.value]

    _view_id = Analysis.plot_view

    def __init__(self):
        """
        Initializes the class with default parameters
        """
        super().__init__(name="path time")

    def analyse(self, data: pd.DataFrame) -> AnalysisDataRecord:
        """
        The analysis uses the _get_distance_time method from the StartEndAnalysis
        :param data: the data to be analysed as a pandas Dataframe
        :returns the analysed data as an AnalysisDataRecord
        """
        data_df = self._get_distance_time(data)

        return AnalysisDataRecord(
            DataRecord(self._name, ('time', 'distance'), data_df[['time', 'distance']]),
            self._view_id
        )
