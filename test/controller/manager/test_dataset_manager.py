import sys
import unittest
from unittest.mock import Mock, MagicMock

import pandas as pd

from src.controller.output_handling.request_manager import InputRequestManager
from src.controller.execution_handling.database_manager import DatabaseManager
from src.data_transfer.content import Column
from src.data_transfer.record import DataRecord
from src.data_transfer.record.selection_record import SelectionRecord
from src.data_transfer.record.setting_record import SettingRecord
from src.data_transfer.exception import InvalidInput
from src.data_transfer.selection.number_interval_option import NumberIntervalOption
from src.database.data_facade import DataFacade


class DatasetManagerTest(unittest.TestCase):
    def setUp(self):
        self.interval_colum = Column.SPEED
        self.discrete_column = Column.SPEED_LIMIT
        self.manager = DatabaseManager()
        self.request_manager = InputRequestManager()
        self.user_input_request = MagicMock()
        self.request_manager.set_user_input_request_facade(self.user_input_request)
        self.manager.set_request_manager(self.request_manager)
        self.data_facade = Mock(DataFacade)
        self.data_facade.get_distinct_data_from_column.return_value = \
            DataRecord(_name="", _column_names=tuple(""),
                       _data=pd.DataFrame({self.interval_colum.value: [30, 50, 60, 50, 30],
                                           self.discrete_column.value: [30, 50, 60, 50, 30]}))
        self.data_facade.get_data.return_value = \
            DataRecord(_name="", _column_names=tuple(""),
                       _data=pd.DataFrame({self.interval_colum.value: [50, 20, 30, 10],
                                           self.discrete_column.value: [50, 20, 30, 10]}))
        self.manager.set_data_facade(self.data_facade)

    def test_get_discrete_selection_column(self):
        """
        Test if the get_discrete_selection_column method returns the expected result of SettingRecord instance.
        """
        result = self.manager.get_discrete_selection_column(self.discrete_column)
        self.assertIsInstance(result, SettingRecord)
        self.assertTrue(all(option in result.selection.option.get_option() for option in [30, 50, 60]))
        self.assertTrue(all(option in [30, 50, 60] for option in result.selection.option.get_option()))

    def test_get_interval_selection_column(self):
        result = self.manager.get_interval_selection_column(self.interval_colum)
        self.assertIsInstance(result.selection.option, NumberIntervalOption)
        self.assertListEqual([-sys.float_info.max, sys.float_info.max], result.selection.option.get_option())

    def test_empty_column_interval(self):
        self.data_facade.get_data.return_value = DataRecord(_name="", _column_names=tuple(""),
                                                            _data=pd.DataFrame({self.interval_colum.value: []}))
        result: SettingRecord = self.manager.get_interval_selection_column(self.interval_colum)
        self.assertIsInstance(result, SettingRecord)
        expected_result = SettingRecord(_context="NUMBER_INTERVAL",
                                        _selection=SelectionRecord(
                                            selected=[[0, 0]],
                                            option=NumberIntervalOption(-sys.float_info.max, sys.float_info.max)
                                        ))
        print(result.selection, expected_result.selection)
        self.assertEqual(result.selection.option, expected_result.selection.option)
        self.assertEqual(result, expected_result)

    def test_not_a_column(self):
        self.assertRaises(InvalidInput, self.manager.get_discrete_selection_column, "not a column")
        self.assertRaises(InvalidInput, self.manager.get_interval_selection_column, "not a column")

    def test_not_correct_column_type(self):
        self.manager.get_discrete_selection_column(Column.SPEED)
        self.user_input_request.send_error.assert_called_with('The column does not fit the filter type  discrete column was expected')
        self.manager.get_interval_selection_column(Column.ROAD_TYPE)
        self.user_input_request.send_error.assert_called_with('The column does not fit the filter type  interval column was expected')



if __name__ == '__main__':
    unittest.main()
