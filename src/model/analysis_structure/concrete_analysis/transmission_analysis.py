import pandas as pd

from src.model.analysis_structure.Analysis import Analysis


class TransmissionFrequencyAnalysis(Analysis):
    """
    This class is used to analyze the transmission frequency of a given dataset.
    It takes in a DataRecord and returns an AnalysisDataRecord with the average
    or distribution of transmission frequency.
    """
    _analysis_types = ["average", "distribution"]
    _view_id = Analysis.histogram_view

    def __init__(self):
        """
       Initializes the class with default parameters
       """
        super().__init__()
        self._required_parameters: [str] = [self.get_column('trajectory_id'), self.get_column('date'),
                                            self.get_column('time')]
        self.setting_name = "analysis type"
        self._set_analysis_record(
            self.create_analysis_record(
                [self.create_setting(name=self.setting_name,
                                     default_selected=[self._analysis_types[0]],
                                     options=self._analysis_types)]
            ))
        self._name = "transmission"

    def analyse(self, data: pd.DataFrame):
        """
        Analyzes the passed data and returns an AnalysisDataRecord. It either analyses the average of the transmission
        frequency per vehicle or it finds how often a given frequency occurs.
        :param data: DataRecord to be analyzed
        :return: AnalysisDataRecord with the result of the analysis
        """
        time_column = self.get_column('time')
        trajectory_id_column = self.get_column('trajectory_id')
        date_column = self.get_column('date')

        data_df = data[[time_column, trajectory_id_column, date_column]]
        data_df['timestamp'] = pd.to_datetime(data_df[date_column] + ' ' + data_df[time_column],
                                              format='%d.%m.%Y %H:%M:%S')
        data_df['time_diff'] = data_df.groupby(trajectory_id_column)['timestamp'].diff()
        data_df['time_diff'] = data_df['time_diff'].dt.total_seconds()

        data_df = data_df[[trajectory_id_column, 'time_diff']]
        analysis_type = self.get_setting_selected(self.setting_name)[0]
        if analysis_type == self._analysis_types[0]:
            return self.to_view_analysis(analysed_data=data_df.groupby(trajectory_id_column)['time_diff']
                                         .mean()
                                         .to_frame()
                                         .reset_index()
                                         .round(1),
                                         view_type=self._view_id,
                                         name=self._name)

        elif analysis_type == self._analysis_types[1]:
            return self.to_view_analysis(analysed_data=self.create_histogram(data_df, 'time_diff').round(1),
                                         view_type=self._view_id,
                                         name=self._name)


CONSTRUCTOR = TransmissionFrequencyAnalysis
