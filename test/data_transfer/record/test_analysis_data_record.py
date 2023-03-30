import unittest

import pandas as pd
from matplotlib.figure import Figure

from src.data_transfer.content.analysis_view import AnalysisViewEnum
from src.data_transfer.record.analysis_data_record import AnalysisDataRecord
from src.data_transfer.record.data_record import DataRecord


class AnalysisDataRecordTest(unittest.TestCase):
    def setUp(self) -> None:
        self.data = DataRecord(_name="analysed data", _column_names=("a", "b"),
                               _data=pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}))
        self.view_id = AnalysisViewEnum.bar_code_view
        self.plot = Figure()

    def test_create_with_data_and_view_id(self):
        """
        tests the creation of an AnalysisDataRecord with data and view id.
        """
        record = AnalysisDataRecord(_data=self.data, _view_id=self.view_id)
        self.assertEqual(self.data, record.data)
        self.assertEqual(self.view_id, record.id)
        self.assertIsNone(record.plot)

    def test_create_with_plot(self):
        """
        tests the creation of an AnalysisDataRecord with plot.
        """
        record = AnalysisDataRecord(_plot=self.plot)
        self.assertIsNone(record.data)
        self.assertIsNone(record.id)
        self.assertEqual(self.plot, record.plot)

    def test_create_with_data_and_view_id_and_plot(self):
        """
        tests the creation of an AnalysisDataRecord with data, view id and plot.
        """
        record = AnalysisDataRecord(_data=self.data, _view_id=self.view_id, _plot=self.plot)
        self.assertEqual(self.data, record.data)
        self.assertEqual(self.view_id, record.id)
        self.assertEqual(self.plot, record.plot)

    def test_create_without_data_and_view_id_and_plot(self):
        """
        tests the creation of an AnalysisDataRecord without data, view id and plot.
        """
        with self.assertRaises(ValueError):
            AnalysisDataRecord()

    def test_create_with_only_data(self):
        """
        tests the creation of an AnalysisDataRecord with only data.
        """
        with self.assertRaises(ValueError):
            AnalysisDataRecord(_data=self.data)

    def test_create_with_only_view_id(self):
        """
        tests the creation of an AnalysisDataRecord with only view id.
        """
        with self.assertRaises(ValueError):
            AnalysisDataRecord(_view_id=self.view_id)


if __name__ == '__main__':
    unittest.main()
