import os
from unittest import TestCase

from pandas import DataFrame
from pandas import Series

from src.file.file.exporter.csv_exporter import CSVExporter
from src.file.file.exporter.feather_exporter import FeatherExporter
from src.file.file.exporter.json_exporter import JSONExporter
from src.file.file.importer.csv_importer import CSVImporter
from src.file.file.importer.feather_importer import FeatherImporter
from src.file.file.importer.json_importer import JSONImporter


class TestExporterImporter(TestCase):
    """
    Test case for testing CSV Importer/Exporter.
    """

    def setUp(self):
        self.csv_exporter = CSVExporter()
        self.csv_importer = CSVImporter()
        self.feather_exporter = FeatherExporter()
        self.feather_importer = FeatherImporter()
        self.json_exporter = JSONExporter()
        self.json_importer = JSONImporter()
        self.csvTempFilePath = os.path.join(os.getcwd(), 'temp.csv')
        self.featherTempFilePath = os.path.join(os.getcwd(), 'temp.feather')
        self.jsonTempFilePath = os.path.join(os.getcwd(), 'temp.json')
        self.data = DataFrame([Series(['test1', 'test2'], index=['col1', 'col2'])])

    def tearDown(self):
        temp_file_paths = [self.csvTempFilePath, self.featherTempFilePath, self.jsonTempFilePath]
        for path in temp_file_paths:
            if os.path.exists(path):
                os.remove(path)

    def test_csv_exporter_importer(self):
        self.csv_exporter.export_data(self.csvTempFilePath, self.data)
        imported_data = self.csv_importer.import_data(self.csvTempFilePath)
        self.assertTrue(all(imported_data == self.data))
        self.assertTrue(os.path.exists(self.csvTempFilePath))

    def test_feather_exporter_importer(self):
        self.feather_exporter.export_data(self.featherTempFilePath, self.data)
        imported_data = self.feather_importer.import_data(self.featherTempFilePath)
        self.assertTrue(all(imported_data == self.data))
        self.assertTrue(os.path.exists(self.featherTempFilePath))

    def test_json_exporter_importer(self):
        self.json_exporter.export_data(self.jsonTempFilePath, self.data)
        imported_data = self.json_importer.import_data(self.jsonTempFilePath)
        self.assertTrue(all(imported_data == self.data))
        self.assertTrue(os.path.exists(self.jsonTempFilePath))
