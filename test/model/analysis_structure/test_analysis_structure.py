import unittest
from unittest.mock import MagicMock
from uuid import UUID
from uuid import uuid4

from pandas import DataFrame

from src.controller.idata_request_facade import IDataRequestFacade
from src.data_transfer.content import Column
from src.data_transfer.exception import InvalidUUID
from src.data_transfer.record import AnalysisDataRecord
from src.data_transfer.record import AnalysisRecord
from src.data_transfer.record import AnalysisTypeRecord
from src.data_transfer.record import DataRecord
from src.model.analysis_structure.analysis_structure import AnalysisStructure
from src.model.analysis_structure.spatial_analysis.path_time_analysis import PathTimeAnalysis
from src.model.polygon_structure.ipolygon_structure import IPolygonStructure
from test.model.analysis_structure.dummy_analysis import DummyAnalysis


class TestAnalysisStructure(unittest.TestCase):
    def setUp(self):
        data_facade_mock = MagicMock(IDataRequestFacade)
        data_facade_mock.get_rawdata.return_value = DataRecord("id_test", tuple([Column.ID]),
                                                               DataFrame({"ID": [uuid4()]}))
        polygon_structure = MagicMock(IPolygonStructure)
        self.structure = AnalysisStructure()
        self.structure.set_data_request(data_facade_mock)
        self.structure.set_polygon_structure(polygon_structure)
        self.dummy_type: AnalysisTypeRecord = self.structure.register_analysis_type(DummyAnalysis)

    def assert_correct_id(self, id: UUID) -> None:
        self.assertIsNotNone(id)

    def test_add_delete_analysis(self):
        analysis_id: UUID = self.structure.create_analysis(self.dummy_type)
        self.assert_correct_id(analysis_id)
        self.assertIsInstance(analysis_id, UUID)
        self.assertIn(analysis_id, self.structure._analysis_map)
        self.structure.delete_analysis(analysis_id)

    def test_de_register_analysis_type(self):
        self.assertIn(self.dummy_type, self.structure.get_analysis_types())
        self.assertTrue(self.structure.de_register_analysis_type(self.dummy_type))
        self.assertNotIn(self.dummy_type, self.structure.get_analysis_types())
        self.assertFalse(self.structure.de_register_analysis_type(self.dummy_type))

    def test_get_analysis_types(self):
        self.assertIsInstance(self.structure.get_analysis_types()[0], AnalysisTypeRecord)

    def test_get_analysed_data(self):
        # set up test
        analysis_id: UUID = uuid4()  # UUID = self.structure.create_analysis(self.dummy_type)
        analysis = MagicMock(DummyAnalysis)
        analysed_data: AnalysisDataRecord = AnalysisDataRecord(MagicMock(DataRecord), "test_id")
        analysis.analyse = MagicMock(return_value=analysed_data)
        self.structure._analysis_map = {analysis_id: analysis}

        # run the test
        result_analysis = self.structure.get_analysed_data(analysis_id)

        # assert
        self.assertIsInstance(result_analysis, AnalysisDataRecord)
        self.assertEqual(result_analysis, analysed_data)
        analysis.analyse.assert_called()
        # assert that it does not work with the wrong id.
        self.assertRaises(InvalidUUID, self.structure.get_analysed_data, uuid4())

    def test_refresh(self):
        analysis_id: UUID = self.structure.create_analysis(self.dummy_type)
        self.assert_correct_id(analysis_id)
        self.assertIsInstance(self.structure.refresh(analysis_id), AnalysisDataRecord)
        self.assertRaises(InvalidUUID, self.structure.refresh, UUID)

    def test_edit_analysis(self):
        # set up test
        analysis_id = uuid4()
        analysis = MagicMock(DummyAnalysis)
        analysis.set_analysis_parameters = MagicMock(return_value=True)
        self.structure._analysis_map = {analysis_id: analysis}
        parameters: AnalysisRecord = AnalysisRecord(tuple())

        # run test
        result = self.structure.edit_analysis(analysis_id, parameters)

        # assert
        self.assertTrue(result)
        analysis.set_analysis_parameters.assert_called_with(parameters)

    def test_get_analysis_parameters(self):
        # set up test
        analysis_id = uuid4()
        analysis = MagicMock(DummyAnalysis)
        analysis_parameter = AnalysisRecord(tuple())
        analysis.get_required_analysis_parameter = MagicMock(return_value=analysis_parameter)
        self.structure._analysis_map = {analysis_id: analysis}

        # run test
        result = self.structure.get_analysis_parameters(analysis_id)

        # assert
        self.assertEqual(result, analysis_parameter)
        analysis.get_required_analysis_parameter.assert_called()

    def test_start_end_analysis_requires_polygon(self):
        path_time_type_record = [analysis_type for analysis_type in self.structure.get_analysis_types()
                                 if analysis_type.name == PathTimeAnalysis().get_name()]
        self.assertEqual(len(path_time_type_record), 1)
        path_time_type_record = path_time_type_record[0]
        analysis_id: UUID = self.structure.create_analysis(path_time_type_record)
        self.assertIsNone(analysis_id)
        errors = self.structure.get_errors()
        self.assertIsNotNone(errors)
        self.assertEqual(len(errors), 1)


if __name__ == '__main__':
    unittest.main()
