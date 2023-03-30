import unittest

from src.data_transfer.content import Column
from src.data_transfer.exception import InvalidInput
from src.data_transfer.record import AnalysisRecord
from src.data_transfer.record import DataRecord
from src.data_transfer.record.selection_record import SelectionRecord
from src.data_transfer.record.setting_record import SettingRecord
from src.data_transfer.selection.discrete_option import DiscreteOption
from src.model.analysis_structure.concrete_analysis.table_analysis import TableAnalysis
from test.model.analysis_structure.concrete_analyses.test_data import TestData


class TestTableAnalysis(unittest.TestCase):

    def setUp(self) -> None:
        self.data: DataRecord = TestData.data[0]
        self.analysis: TableAnalysis = TableAnalysis()
        self.analysis_record = AnalysisRecord(
            _required_data=(
                SettingRecord(
                    _identifier="",
                    _context=TableAnalysis().setting_name,
                    _selection=SelectionRecord(
                        selected=list(self.data.data.columns),
                        option=DiscreteOption(Column.val_list()),
                        possible_selection_range=range(1, len(Column.val_list()) + 1)
                    )
                ),
            )
        )
        self.analysis.set_analysis_parameters(self.analysis_record)

    def test_analysis(self):
        """
        This test case tests that the TableAnalysis gives back the exact same Data that it was passed.
        :return:
        """
        self.assertTrue(self.data.data.equals(self.analysis.analyse(self.data.data).data.data))
        self.assertDictEqual(self.data.data.to_dict(), self.analysis.analyse(self.data.data).data.data.to_dict())

    def test_get_required_columns(self):
        """
        This test case tests the get_required_columns method of the TableAnalysis class,
        by getting the required columns and checking if they are of the type Column.
        """
        columns = self.analysis.get_required_columns()
        for column in columns:
            self.assertIsInstance(Column.get_column_from_str(column), Column)

    def test_get_required_parameter(self):
        """
        This test case tests the get_required_parameter method of the TableAnalysis class,
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
                            selected=self.data.data.columns.to_list(),
                            option=DiscreteOption(Column.val_list()),
                            possible_selection_range=range(1, len(Column.list()) + 1)
                        )
                    ),
                    SettingRecord(
                        _identifier="",
                        _context="parameters",
                        _selection=SelectionRecord(
                            selected=self.data.data.columns.to_list(),
                            option=DiscreteOption(Column.val_list()),
                            possible_selection_range=range(1, len(Column.list()) + 1)
                        )
                    )
                )
            )]

        for i, invalid_record in enumerate(invalid_cases):
            with self.subTest(i=i):
                self.assertRaises(InvalidInput, self.analysis.set_analysis_parameters, invalid_record)


if __name__ == '__main__':
    unittest.main()
