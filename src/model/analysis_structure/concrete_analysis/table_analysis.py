import pandas as pd

from src.data_transfer.record import AnalysisDataRecord
from src.model.analysis_structure.Analysis import Analysis


class TableAnalysis(Analysis):
    """
    Analysis to display selected columns in a table view.
    """
    _view_id = Analysis.table_view

    def __init__(self):
        """
        Initializes the class and sets the default parameters for the analysis.
        """
        super().__init__()
        self.setting_name = "columns"
        self._set_analysis_record(
            self.create_analysis_record(
                [self.create_setting(name=self.setting_name,
                                     default_selected=[self.get_column('id'), self.get_column("trajectory_id"),
                                                       self.get_column('date'),
                                                       self.get_column('longitude'), self.get_column('latitude'),
                                                       self.get_column("speed"), self.get_column('acceleration')],
                                     options=self.get_all_columns(),
                                     possible_selection_range=range(1, len(self.get_all_columns()) + 1))]
            ))
        self._name: str = "table"

    def set_analysis_parameters(self, record) -> bool:
        """
        Sets the parameters of the analysis from the record.
        :param record: The AnalysisRecord that contains the possible parameters.
        :returns True if the operation was successful.
        """
        super().set_analysis_parameters(record)
        self.set_required_columns(self.get_columns_from_setting(self.setting_name))
        return True

    def analyse(self, data: pd.DataFrame):
        """
        Analyze the input data and return an AnalysisDataRecord containing the results

        :param data: DataFrame containing the data to be analyzed
        :type data: DataFrame
        :return: AnalysisDataRecord containing the results of the analysis
        :rtype: AnalysisDataRecord
        """
        return self.to_view_analysis(
            analysed_data=data[self.get_columns_from_setting(self.setting_name)],
            view_type=self._view_id,
            name=self._name
        )


CONSTRUCTOR = TableAnalysis
