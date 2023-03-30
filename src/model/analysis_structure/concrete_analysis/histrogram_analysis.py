import pandas as pd

from src.model.analysis_structure.Analysis import Analysis


class HistogramAnalysis(Analysis):
    """
    Analysis to create histograms for columns.
    """
    _view_id = Analysis.histogram_view

    def __init__(self):
        """
        Initializes the class and sets the default parameters for the analysis.
        """
        super().__init__()
        self.setting_name = "column"
        self._set_analysis_record(
            self.create_analysis_record(
                [self.create_setting(name=self.setting_name,
                                     default_selected=[self.get_column("speed")],
                                     options=self.get_all_columns())]
            ))
        self._name = "histogram"

    def set_analysis_parameters(self, record) -> bool:
        """
        Sets the parameters of the analysis from the record.
        :param record: The record that contains the possible parameters.
        :returns True if the operation was successful.
        """
        super().set_analysis_parameters(record)
        self.set_required_columns(self.get_columns_from_setting(self.setting_name))
        return True

    def analyse(self, data: pd.DataFrame):
        """
        Analyzes the input data and returns a histogram of the selected data.
        :param data: DataFrame containing the data to be analyzed.
        :return: AnalysisDataRecord containing the histogram of the selected data.
        It also includes the id of the view the data is supposed to be displayed as.
        """
        return self.to_view_analysis(
            analysed_data=self.create_histogram(data, self.get_columns_from_setting(self.setting_name)[0]),
            view_type=self._view_id,
            name=self._name)


CONSTRUCTOR = HistogramAnalysis
