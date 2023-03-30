import pandas as pd

from src.data_transfer.content import Column
from src.data_transfer.record import AnalysisDataRecord
from src.data_transfer.record import DataRecord
from src.model.analysis_structure.Analysis import Analysis
from src.model.analysis_structure.spatial_analysis.start_end_analysis import StartEndAnalysis


class PathDaytimeAnalysis(StartEndAnalysis):
    """
    This class prepares the data for the path daytime analysis. It prepares to columns to be plotted against each other:
    The time vs the distance taken. Here the time is not relative to the start of the analysis but instead the absolute
    daytime.
    """

    _columns = [Column.TRAJECTORY_ID.value, Column.DATE.value, Column.TIME.value, Column.LONGITUDE.value,
                Column.LATITUDE.value]

    _view_id = Analysis.path_daytime

    def __init__(self):
        """
        Initializes the class with default parameters
        """
        super().__init__(name="path daytime")

    def analyse(self, data: pd.DataFrame) -> AnalysisDataRecord:
        """
        Analyses the data by calling the get_distance_time method from the StartEndAnalysis and replacing the relative
        time with the absolute time.
        :param data: The data as a pandas dataframe containing at least the columns specified in the _columns attribute.
        :return: An AnalysisDataRecord with three column, the id, daytime and distance traveled.
        """
        data_df = self._get_distance_time(data.copy())
        data_df[Column.TIME.value] = data[Column.TIME.value]

        return AnalysisDataRecord(
            DataRecord(self._name, (Column.TRAJECTORY_ID.value, Column.TIME.value, 'distance'),
                       data_df[[Column.TRAJECTORY_ID.value, Column.TIME.value, 'distance']]),
            self._view_id
        )
