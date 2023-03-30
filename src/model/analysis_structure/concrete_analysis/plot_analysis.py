import pandas as pd

from src.model.analysis_structure.Analysis import Analysis


class PlotAnalysis(Analysis):
    """
    This class is used to plot two selected attributes against each other in a graph.
    """

    _view_id = Analysis.plot_view

    def __init__(self):
        """
        Initializes the class with default parameters
        """
        super().__init__()
        self._x_attribute = "x axis attribute"
        self._y_attribute = "y axis attribute"
        self._set_analysis_record(
            self.create_analysis_record(
                [self.create_setting(name=self._x_attribute,
                                     default_selected=[self.get_column(column_name="speed_limit")],
                                     options=self.get_all_columns(),
                                     ),
                 self.create_setting(name=self._y_attribute,
                                     default_selected=[self.get_column(column_name='time')],
                                     options=self.get_all_columns()
                                     )
                 ]
            ))
        self._name = "plot"

    def set_analysis_parameters(self, record) -> bool:
        """
        Set the analysis parameters with the passed record
        :param record: record with analysis parameters
        :return: True if the record is valid and parameters are set
        """
        super().set_analysis_parameters(record=record)
        self.set_required_columns(
            [self.get_setting_selected(setting_name=self._x_attribute)[0],
             self.get_setting_selected(setting_name=self._y_attribute)[0]]
        )
        return True

    def analyse(self, data: pd.DataFrame):
        """
        Analyzes the data by plotting the two specified attributes. The first attribute is considered as the x-value
        and the second attribute is considered as the y-value.
        :param data: data to be analyzed as a pandas DataFrame
        :return: result of the analysis as an AnalysisDataRecord
        """
        x_column = self.get_columns_from_setting(self._x_attribute)[0]
        y_column = self.get_columns_from_setting(self._y_attribute)[0]
        xy_values = data[[x_column, y_column]]

        return self.to_view_analysis(analysed_data=xy_values,
                                     view_type=self._view_id,
                                     name=self._name)


CONSTRUCTOR = PlotAnalysis
