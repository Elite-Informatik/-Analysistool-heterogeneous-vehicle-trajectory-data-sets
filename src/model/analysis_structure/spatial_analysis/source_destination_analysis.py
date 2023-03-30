import pandas as pd

from src.data_transfer.content import Column
from src.data_transfer.record import AnalysisDataRecord
from src.data_transfer.record import DataRecord
from src.model.analysis_structure.Analysis import Analysis
from src.model.analysis_structure.spatial_analysis.start_end_analysis import StartEndAnalysis


class SourceDestinationAnalysis(StartEndAnalysis):
    """
    This class prepares the data for the source destination analysis. It calculates the time taken from the start to the
    end polygon, the distance, as well as the average speed.
    It does this for each trajectory individually and also calculates the mean.
    """

    _columns = [Column.TRAJECTORY_ID.value, Column.DATE.value, Column.TIME.value, Column.LONGITUDE.value,
                Column.LATITUDE.value]

    _view_id = Analysis.table_view

    def __init__(self):
        """
        Initializes the class with default parameters
        """
        super().__init__(name="source destination")

    def analyse(self, data: pd.DataFrame) -> AnalysisDataRecord:
        """
        Calculates the time taken, distance driven and average speed of each trajectory and
        :param data: The data to be analysed as a DataRecord
        :return: The analysed data as an AnalysisDataRecord
        """
        ms_to_kmh = 3.6
        data_df = self._get_distance_time(data)
        data_df = data_df.groupby(Column.TRAJECTORY_ID.value)['time', 'distance'].last()
        data_df.loc['mean'] = data_df.mean()
        data_df['average_speed'] = (data_df['distance'] / data_df['time']) * ms_to_kmh
        data_df['time'] = pd.to_datetime(data_df["time"], unit='s').dt.strftime("%H:%M:%S")
        data_df = data_df.reset_index().round()

        return AnalysisDataRecord(
            DataRecord(self._name, data_df.columns.names, data_df),
            self._view_id
        )
