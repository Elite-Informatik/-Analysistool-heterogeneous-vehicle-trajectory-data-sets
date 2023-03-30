import pandas as pd

from src.model.analysis_structure.Analysis import Analysis


class TotalParameterAnalysis(Analysis):
    """
    Analysis to calculate the number of unique values in non-numeric columns. For numeric columns it rounds
    to one place after the period and then counts unique values.
    """

    _view_id = Analysis.table_view

    def __init__(self):
        """
        Initializes the class and sets the default parameters for the analysis.
        """
        super().__init__()
        self.setting_name: str = "column"
        self._set_analysis_record(
            self.create_analysis_record(
                [self.create_setting(name=self.setting_name,
                                     default_selected=[self.get_column("speed")],
                                     options=self.get_all_columns(),
                                     possible_selection_range=range(1, len(self.get_all_columns()) + 1))]
            ))
        self._name: str = "total parameter"

    def set_analysis_parameters(self, record) -> bool:
        """
        Sets the parameters of the analysis from the record.
        :param record: The AnalysisRecord that contains the possible parameters.
        :returns True if the operation was successful.
        """
        super().set_analysis_parameters(record)
        self._required_parameters = self.get_columns_from_setting(self.setting_name)
        return True

    def analyse(self, data: pd.DataFrame):
        """
        Analyze the input data and return an AnalysisDataRecord containing the results

        :param data: DataFrame containing the data to be analyzed
        :return: AnalysisDataRecord containing the results of the analysis
        """
        return self.to_view_analysis(analysed_data=self.find_unique_values(data, 1),
                                     view_type=self._view_id,
                                     name=self._name)


CONSTRUCTOR = TotalParameterAnalysis
