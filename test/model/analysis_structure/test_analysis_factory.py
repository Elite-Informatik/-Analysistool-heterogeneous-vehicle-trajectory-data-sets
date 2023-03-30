import unittest
from unittest.mock import MagicMock
from uuid import uuid4

from src.data_transfer.exception.custom_exception import IllegalAnalysisError
from src.data_transfer.record import AnalysisRecord
from src.model.analysis_structure.analysis_factory import AnalysisFactory
from test.model.analysis_structure.dummy_analysis import DummyAnalysis


class NotAnalysis:
    """
    Not an analysis. Used for testing.
    """
    pass


class TestAnalysisFactory(unittest.TestCase):
    def setUp(self):
        self.factory = AnalysisFactory()
        self.mock_analysis_record = MagicMock(spec=AnalysisRecord)

    def test_register_analysis(self):
        mock_id = self.factory.register_analysis(DummyAnalysis)
        self.assertIn(mock_id, self.factory._analysis_map)
        self.assertEqual(self.factory._analysis_map[mock_id], DummyAnalysis)

    def test_de_register_analysis(self):
        mock_id = uuid4()
        self.factory._analysis_map[mock_id] = DummyAnalysis
        self.assertTrue(self.factory.de_register_analysis(mock_id))
        self.assertNotIn(mock_id, self.factory._analysis_map)

    def test_create_analysis(self):
        mock_id = uuid4()
        self.factory._analysis_map[mock_id] = DummyAnalysis
        self.assertIsInstance(self.factory.create_analysis(mock_id), DummyAnalysis)

    def test_not_constructable(self):
        self.assertRaises(Exception, self.factory.register_analysis, "not an analysis")

    def test_constructable_not_analysis(self):
        try:
            self.factory.register_analysis(NotAnalysis)
        except(IllegalAnalysisError):
            return
        self.fail("not raises.")


if __name__ == '__main__':
    unittest.main()
