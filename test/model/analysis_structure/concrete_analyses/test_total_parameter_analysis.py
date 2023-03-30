import unittest

import pandas as pd

from src.data_transfer.content import Column
from src.data_transfer.exception import InvalidInput
from src.data_transfer.record import AnalysisRecord
from src.data_transfer.record import DataRecord
from src.data_transfer.record.selection_record import SelectionRecord
from src.data_transfer.record.setting_record import SettingRecord
from src.data_transfer.selection.discrete_option import DiscreteOption
from src.model.analysis_structure.concrete_analysis.parameter_analysis_total import TotalParameterAnalysis


class TestTotalParameterAnalysis(unittest.TestCase):

    def setUp(self):
        """
        This method is run at the beginning of each test, it sets up the basic required data for all the test cases.
        """
        self.columns = [Column.SPEED.value, Column.TRAJECTORY_ID.value, Column.ACCELERATION.value]
        self.data = DataRecord("Test data", tuple(self.columns), pd.DataFrame({
            Column.SPEED.value: [1, 2, 3, 4, 2],
            Column.TRAJECTORY_ID.value: ["a", "b", "c", "d", "e"],
            Column.ACCELERATION.value: [1.1, 2.22, 2.23, 2.2, 1.25]
        }))
        self.analysis_record = AnalysisRecord(
            _required_data=(
                SettingRecord(
                    _identifier="",
                    _context="column",
                    _selection=SelectionRecord(
                        selected=self.columns,
                        option=DiscreteOption(Column.val_list()),
                        possible_selection_range=range(1, len(Column.val_list()) + 1)
                    )
                ),
            )
        )

        self.analysis = TotalParameterAnalysis()
        self.analysis.set_analysis_parameters(self.analysis_record)

    def test_analyse(self):
        """
        This test case tests the analyse method of the TotalParameterAnalysis class, by passing it a valid data record
        and comparing the output with the expected output.
        """
        result = self.analysis.analyse(self.data.data)
        self.assertEqual(result.data.data[Column.SPEED.value]["Total"], 4)
        self.assertEqual(result.data.data[Column.TRAJECTORY_ID.value]["Total"], 5)
        self.assertEqual(result.data.data[Column.ACCELERATION.value]["Total"], 3)

    def test_get_required_columns(self):
        """
        This test case tests the get_required_columns method of the TotalParameterAnalysis class,
        by getting the required columns and checking if they are of the type Column.
        """
        columns = self.analysis.get_required_columns()
        for column in columns:
            self.assertIsInstance(Column.get_column_from_str(column), Column)

    def test_get_required_parameter(self):
        """
        This test case tests the get_required_parameter method of the TotalParameterAnalysis class,
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
                        _context="parameters",
                        _selection=SelectionRecord(
                            selected=self.columns,
                            option=DiscreteOption(Column.val_list()),
                            possible_selection_range=range(1, len(Column.val_list()) + 1)
                        )
                    )
                )
            )
        ]

        for i, invalid_record in enumerate(invalid_cases):
            with self.subTest(i=i):
                self.assertRaises(InvalidInput, self.analysis.set_analysis_parameters, invalid_record)


if __name__ == '__main__':
    unittest.main()
