from abc import ABC
from abc import abstractmethod
from typing import Dict
from typing import List
from typing import Optional

import pandas as pd
from matplotlib.figure import Figure
from numpy import dtype

from src.data_transfer.content import Column
from src.data_transfer.content.analysis_view import AnalysisViewEnum
from src.data_transfer.exception import InvalidInput
from src.data_transfer.record import AnalysisDataRecord
from src.data_transfer.record import AnalysisRecord
from src.data_transfer.record import DataRecord
from src.data_transfer.record.selection_record import SelectionRecord
from src.data_transfer.record.setting_record import SettingRecord
from src.data_transfer.selection.discrete_option import DiscreteOption


class Analysis(ABC):
    """
    Analyses are responsible for analyzing and evaluating filtered data.
    The abstract analysis class defines how an analysis should look.
    In addition, only the Analysis class and classes from the data_transfer module should be used.
    It includes the following methods:
    """

    def __init__(self):
        self._required_parameters: List[str] = Column.val_list()
        self.analysis_record: Optional[AnalysisRecord] = None
        self.template_analysis_record: Optional[AnalysisRecord] = None
        self._name: str = "default name"

    def get_required_columns(self) -> List[str]:
        """
        Returns the required columns that the analysis needs from the database.
        This way, not the entire dataset needs to be passed, only a part,
        thus avoiding unnecessary use of memory with data that the analysis does not need.
        """
        return self._required_parameters

    @abstractmethod
    def analyse(self, data_df: pd.DataFrame) -> AnalysisDataRecord:
        """
        Analyzes the given data and packages it into an AnalyseDataRecord.
        This includes the analyzed data and how it should be displayed.
        The ID for the display is stored statically in the respective analysis.
        """
        raise NotImplementedError

    def get_required_analysis_parameter(self) -> AnalysisRecord:
        """
        Creates an AnalysisRecord. The record includes the selections that need to be made to create an analysis
        as well as the _name of the analysis.
        This is then given outwards and used later to create the analysis.
        """
        return self.analysis_record

    def get_name(self) -> str:
        """
        Returns the _name of the Analysis
        :returns: a string representing the _name of the analysis.
        """
        return self._name

    def set_analysis_parameters(self, record: AnalysisRecord) -> bool:
        """
        Sets the analysis parameter contained in the AnalysisRecord.
        :param record: The AnalysisRecord containing the choices made by the user.
        :return: True if it was successful.
        """
        given_settings = record.required_data
        expected_settings = self.template_analysis_record.required_data
        if len(given_settings) != len(expected_settings):
            raise InvalidInput(f"{len(given_settings)} settings were given, "
                               f"but {len(expected_settings)} were expected")
        for given_setting, expected_settings in zip(given_settings, expected_settings):
            if given_setting.context != expected_settings.context:
                raise InvalidInput(f"Expected context: {expected_settings.context}, "
                                   f"but {given_setting.context} was given.")

            given_selection, expected_selection = given_setting.selection, expected_settings.selection
            if not expected_selection.check_equal_type(given_selection):
                raise InvalidInput(f"The given selection {given_selection}, "
                                   f"does not match the expected selection: {expected_selection}")
        self.analysis_record = record
        return True

    @classmethod
    def find_unique_values(cls, data: pd.DataFrame, precision: int) -> pd.DataFrame:
        """
        Finds the number of unique values in non-numeric columns. For numeric columns it rounds
        to one place after the period and then counts unique values.
        :param precision: The precision to which floats will be rounded for finding unique values.
        :param data: The data to be analysed as a DataRecord.
        :return: The DataRecord containing the data unique value pairs.
        """
        # Create a dataframe from the input data
        data_df = data.copy()

        # Select only the parameters that are selected for analysis and round them if necessary to one decimal place
        data_df = data_df.round(precision)
        # Initialize a dictionary to store the results
        result = {}
        # For each parameter, count the number of unique values
        for column in data_df.columns:
            result[column] = data_df[column].nunique()
        # Create a dataframe from the result
        result_df = pd.DataFrame(result, index=["Total"])
        # Return the analysis data in the form of an AnalysisDataRecord
        return result_df

    def calculate_average_mode(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Finds the average of numeric columns and mode of non-numeric columns.
        :param data: The data to be analysed as a DataRecord.
        :return: The DataRecord containing the data average/mode pairs.
        """
        # Create a dataframe from the input data
        data_df = data.copy()
        # Store the dtype of each parameter
        param_types: Dict[str, dtype] = {param: data_df[param].dtype for param in data_df.columns}
        # Calculate the mean of the numeric columns
        result = data_df.select_dtypes(include=['float64', 'int64']).mean().to_frame().transpose()
        # For each non-numeric parameter, select the mode value
        for param in data_df.columns:
            if param_types[param] == 'object':
                result[param] = data_df[param].mode().values[0]
        # Create a dataframe from the result
        result_df = pd.DataFrame(result)
        # Return the analysis data in the form of an AnalysisDataRecord
        return result_df

    @classmethod
    def create_histogram(cls, data: pd.DataFrame, column) -> pd.DataFrame:
        """
        Counts the occurrences of each value in the data and creates a new data record with the values.
        :param data: The data to be analysed as a DataRecord.
        :param column: The data from the data to be analysed.
        :return: The DataRecord containing the value occurrence pairs.
        """
        # Create a dataframe from the input data
        data_df = pd.DataFrame(data)
        # Count the number of occurrences of each value
        value_counts = data_df[column].value_counts()
        # Transpose the Data, so it matches the expected data format of the histogram analysis
        result_df = value_counts.to_frame().reset_index().rename(columns={'index': column, 'count': 'Occurrence'})
        # Return the data
        return result_df

    @property
    def histogram_view(self):
        """
        A property to be used if an analysis wants to use the histogram analysis view. It adds the return of this method
        to the AnalysisDataRecord for the view to know which analysis view is expected to be used.
        :return: The enum entry of the histogram view.
        """
        return AnalysisViewEnum.histogram_view

    @property
    def plot_view(self):
        """
        A property to be used if an analysis wants to use the plot analysis view. It adds the return of this method
        to the AnalysisDataRecord for the view to know which analysis view is expected to be used.
        :return: The enum entry of the plot view.
        """
        return AnalysisViewEnum.plot_view

    @property
    def table_view(self):
        """
        A property to be used if an analysis wants to use the table analysis view. It adds the return of this method
        to the AnalysisDataRecord for the view to know which analysis view is expected to be used.
        :return: The enum entry of the table view.
        """
        return AnalysisViewEnum.table_view

    @property
    def heatmap_view(self):
        """
        A property to be used if an analysis wants to use the heatmap analysis view. It adds the return of this method
        to the AnalysisDataRecord for the view to know which analysis view is expected to be used.
        :return: The enum entry of the heatmap view.
        """
        return AnalysisViewEnum.heatmap_view

    @property
    def path_daytime(self):
        """
        A property to be used if an analysis wants to use the path daytime analysis view. It adds the return of this
        method to the AnalysisDataRecord for the view to know which analysis view is expected to be used.
        :return: The enum entry of the heatmap view.
        """
        return AnalysisViewEnum.bar_code_view

    @classmethod
    def get_column(cls, column_name: str) -> str:
        """
        Checks if the passed column name is a valid column and returns the name of the column as string.
        :param column_name: The name of the column from which the column is gotten.
        :return: The value of the requested column if valid.
        :raises: ValueError if the column that was passed is not in the database.
        """
        column = Column.get_column_from_str(column_str=column_name)
        if column is None:
            raise ValueError(f"The column {column_name} is not a valid column. Valid columns are: {Column.val_list()}")
        return column.value

    @classmethod
    def get_all_columns(cls) -> List[str]:
        """
        :returns: All the columns in the database as a list of str.
        """
        return Column.val_list()

    @classmethod
    def get_numeric_columns(cls) -> List[str]:
        """
        :returns: All the numeric columns in the database as a list of str.
        """
        return [column.value for column in Column.get_number_interval_columns()]

    @classmethod
    def create_setting(cls, name: str, default_selected: [], options: [],
                       possible_selection_range: range = range(1, 2)) -> SettingRecord:
        """
        Creates a setting from which the user can choose from a given set of options.
        :param name: the name of the setting by which it will be identified.
        :param default_selected: A list of default selected options.
        :param options: The total list of possibly selectable options.
        :param possible_selection_range: The range of the amount of options that are validly selectable.
        :return: a SettingRecord containing the passed parameters.
        """
        return SettingRecord(_selection=SelectionRecord(selected=default_selected,
                                                        option=DiscreteOption(options=options),
                                                        possible_selection_range=possible_selection_range),
                             _context=name)

    @classmethod
    def create_analysis_record(cls, settings: List[SettingRecord]) -> AnalysisRecord:
        """
        Creates an analysis record from the list of settings passed.
        :param settings: The list of settings that will be combined to an AnalysisRecord
        :return: the AnalysisRecord containing the Settings.
        """
        return AnalysisRecord(tuple(settings))

    def _set_analysis_record(self, analysis_record: AnalysisRecord) -> None:
        """
        A protected method used by the subclasses to initially set the parameters.
        Later if new options are set, it is compared to the initial record to check for validity.
        :param analysis_record: the record containing the possible options as well as a default selected subset.
        :return:
        """
        self.analysis_record = analysis_record
        if self.template_analysis_record is None:
            self.template_analysis_record = analysis_record

    def get_setting_selected(self, setting_name: str) -> Optional[List]:
        """
        Gets a list of the selection the user made for the setting specified by the setting_name
        :param setting_name: The name of the setting that the selection is requested from.
        :return: An Optional list of the selections made. If the no setting exists with the given name None is returned,
                    else the list of selections made.
        """
        matched_settings = [setting for setting in self.analysis_record.required_data
                            if setting.context == setting_name]
        if len(matched_settings) == 0:
            return None
        return matched_settings[0].selection.selected

    def get_columns_from_setting(self, setting_name: str) -> List[str]:
        """
        Returns the selected columns inside a setting if that setting contains valid selected columns.
        :param setting_name: The name of the setting to extract the selected columns from.
        :return: a list of the columns as strings.
        """
        return [self.get_column(column_name=selected_column)
                for selected_column in self.get_setting_selected(setting_name=setting_name)]

    def set_required_columns(self, column_names: List[str]) -> None:
        """
        Sets the required columns of the analysis.
        :param column_names: The names of the settings that include columns
        """
        self._required_parameters = [Column.get_column_from_str(column_str).value for column_str in column_names]

    @classmethod
    def to_view_analysis(cls, analysed_data: pd.DataFrame, view_type: AnalysisViewEnum,
                         name: str = "analysed data") -> AnalysisDataRecord:
        """
        Fills in the necessary parameters to convert the Data to a format that can be read by the view.
        :param analysed_data: The data as a DataFrame analyzed by the analysis.
        :param view_type: The type of view that is chosen to display the analysis.
        :param name: The name of the analysis to be displayed in the view
        :return: the data as an AnalysisDataRecord to be transferred to the view
        """
        return AnalysisDataRecord(_data=DataRecord(_data=analysed_data,
                                                   _column_names=tuple(analysed_data.columns.to_list()),
                                                   _name=name),
                                  _view_id=view_type)

    @classmethod
    def to_view_analysis_plot(cls, plot: Figure) -> AnalysisDataRecord:
        """
        Fills in the necessary parameters to convert the Data to a format that can be read by the view.
        :param plot: The plot as a Figure.
        :return: the data as an AnalysisDataRecord to be transferred to the view.
        """
        return AnalysisDataRecord(_plot=plot)


CONSTRUCTOR = Analysis
