from unittest import TestCase

from src.data_transfer.record.selection_record import SelectionRecord


class SelectionTest(TestCase):
    def test_selection_record_exeptions(self):
        with self.assertRaises(TypeError):
            SelectionRecord()
