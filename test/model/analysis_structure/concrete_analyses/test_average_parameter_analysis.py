import unittest

import pandas as pd

from src.data_transfer.content import Column
from src.data_transfer.content.analysis_view import AnalysisViewEnum
from src.data_transfer.exception import InvalidInput
from src.data_transfer.record import AnalysisDataRecord
from src.data_transfer.record import AnalysisRecord
from src.data_transfer.record import DataRecord
from src.data_transfer.record.selection_record import SelectionRecord
from src.data_transfer.record.setting_record import SettingRecord
from src.data_transfer.selection.discrete_option import DiscreteOption
from src.model.analysis_structure.concrete_analysis.parameter_analysis_average import AverageParameterAnalysis


class TestAverageParameterAnalysis(unittest.TestCase):
    """
    Test class for the Average parameter analysis.
    """

    def setUp(self):
        """
        This method is run at the beginning of each test, it sets up the basic required data for all the test cases
        """
        self.columns = [Column.SPEED.value, Column.ACCELERATION.value, Column.TRAJECTORY_ID.value]
        self.analysis_record = AnalysisRecord(
            _required_data=(
                SettingRecord(
                    _identifier="",
                    _context=AverageParameterAnalysis().setting_name,
                    _selection=SelectionRecord(
                        selected=self.columns,
                        option=DiscreteOption(Column.val_list()),
                        possible_selection_range=range(1, len(Column.list()) + 1)
                    )
                ),
            )
        )
        self.analysis = AverageParameterAnalysis()
        self.analysis.set_analysis_parameters(self.analysis_record)
        self.data = {Column.SPEED.value: [1, 2, 3], Column.ACCELERATION.value: [4, 5, 18],
                     Column.TRAJECTORY_ID.value: ['a', 'a', 'b']}
        self.data_df = pd.DataFrame(self.data)
        self.data_record = DataRecord("data", tuple(self.columns), self.data_df)

    def test_analyse_success(self):
        """
        This test case tests the analyse method of the AverageParameterAnalysis class, by passing it a valid data record
        and comparing the output with the expected output.
        """
        result = self.analysis.analyse(self.data_record.data)
        expected_result = AnalysisDataRecord(
            DataRecord("analysed data", tuple(self.columns),
                       pd.DataFrame(
                           data={Column.SPEED.value: [2.0], Column.ACCELERATION.value: [9.0],
                                 Column.TRAJECTORY_ID.value: ['a']})),
            AnalysisViewEnum.table_view
        )

        pd.testing.assert_frame_equal(result.data.data, expected_result.data.data)

    def test_get_required_columns(self):
        """
        This test case tests the get_required_columns method of the AverageParameterAnalysis class,
        by getting the required columns and checking if they are of the type Column.
        """
        columns = self.analysis.get_required_columns()
        for column in columns:
            self.assertIsInstance(Column.get_column_from_str(column), Column)

    def test_get_required_parameter(self):
        """
        This test case tests the get_required_parameter method of the AverageParameterAnalysis class,
        by getting the required analysis parameters and checking if they are set correctly.
        """
        self.assertTrue(self.analysis.set_analysis_parameters(self.analysis.get_required_analysis_parameter()))

    def test_analyze_failure_invalid_parameter(self):
        """
        Test that an exception is raised when trying to analyse with an invalid analysis record
        """

        invalid_cases = [
            # record does not contain the correct amount of option
            AnalysisRecord(
                _required_data=(
                    SettingRecord(
                        _identifier="",
                        _context="parameters",
                        _selection=SelectionRecord(
                            selected=self.columns,
                            option=DiscreteOption(Column.val_list()),
                            possible_selection_range=range(1, len(Column.val_list()) + 1)
                        )
                    ),
                    SettingRecord(
                        _identifier="",
                        _context="column",
                        _selection=SelectionRecord(
                            selected=self.columns,
                            option=DiscreteOption(Column.val_list()),
                            possible_selection_range=range(1, len(Column.list()) + 1)
                        )
                    )
                )
            ),
            # no parameter was selected in the record
            AnalysisRecord(
                _required_data=(
                    SettingRecord(
                        _identifier="",

                        _context="column",
                        _selection=SelectionRecord(
                            selected=[],
                            option=DiscreteOption(Column.val_list()),
                            possible_selection_range=range(0, 1)
                        )
                    ),
                )
            ),
        ]

        for i, invalid_record in enumerate(invalid_cases):
            with self.subTest(i=i):
                self.assertRaises(InvalidInput, self.analysis.set_analysis_parameters, invalid_record)


if __name__ == '__main__':
    unittest.main()
