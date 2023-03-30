import pandas as pd

from src.model.analysis_structure.Analysis import Analysis


class HeatmapAnalysis(Analysis):
    """A heatmap analysis class to represent a heatmap visualization.

    Attributes:
        _view_id (view enum): The view id for heatmap visualization.
        _x_attribute (str): The name of the setting that selects the x attribute.
        _y_attribute (str): The name of the setting that selects the y attribute.
        _color_attribute (str): The name of the setting that selects the color attribute.
        _name (str): The _name of the heatmap analysis.
    """
    _view_id = Analysis.heatmap_view

    def __init__(self):
        """Initialize the heatmap analysis."""
        super().__init__()
        self._x_attribute = "x axis attribute"
        self._y_attribute = "y axis attribute"
        self._color_attribute = "color attribute"
        self._set_analysis_record(
            self.create_analysis_record(
                [self.create_setting(name=self._x_attribute,
                                     default_selected=[self.get_column(column_name="speed_limit")],
                                     options=self.get_all_columns(),
                                     ),
                 self.create_setting(name=self._y_attribute,
                                     default_selected=[self.get_column(column_name='time')],
                                     options=self.get_all_columns()
                                     ),
                 self.create_setting(name=self._color_attribute,
                                     default_selected=[self.get_column(column_name='speed')],
                                     options=self.get_all_columns()
                                     )
                 ]
            ))
        self._name = "heatmap"

    def set_analysis_parameters(self, record):
        """
        This method sets the specified attributes to be plotted in the heatmap.
        The attributes should be specified in the `record` object.
        """
        super().set_analysis_parameters(record=record)
        self.set_required_columns(
            [self.get_setting_selected(setting_name=setting_name)[0]
             for setting_name in [self._x_attribute, self._y_attribute, self._color_attribute]])

        return True

    def analyse(self, data_df: pd.DataFrame):
        """
        This method takes a `DataFrame` object as input and returns an `AnalysisDataRecord` object
        as output.
        :param: data_record: The `DataRecord` object is used to conduct the analysis.
        """
        round_to = 3
        x_column = self.get_columns_from_setting(self._x_attribute)[0]
        y_column = self.get_columns_from_setting(self._y_attribute)[0]
        color_column = self.get_columns_from_setting(self._color_attribute)[0]
        data: pd.DataFrame = data_df[[x_column, y_column, color_column]].round(round_to)
        if color_column in self.get_numeric_columns():
            data = data.pivot_table(index=y_column,
                                    columns=x_column,
                                    values=color_column)
        else:
            data = data.pivot_table(index=y_column,
                                    columns=x_column,
                                    values=color_column,
                                    aggfunc='count')
        data = data.fillna(value=0)

        return self.to_view_analysis(analysed_data=data, view_type=self._view_id, name=self._name)


CONSTRUCTOR = HeatmapAnalysis
