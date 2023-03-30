import json
import os
from unittest import TestCase

from pandas import DataFrame

from src.file.file.exporter.json_exporter import JSONExporter


class TestJSONExporter(TestCase):

    def setUp(self):
        self.source_file = os.path.join(os.getcwd(), 'test_file.json')
        self.exporter = JSONExporter()

    def test_get_file_format(self):
        self.assertEqual(self.exporter.get_file_format(), 'json',
                         'Should get file format.')

    def test_export_data(self):
        test_data = DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        self.exporter.export_data(self.source_file, test_data)
        with open(self.source_file, 'r') as file:
            data = json.load(file)
            self.assertEqual(len(data), 3,
                             'Should export data correctly.')

    def tearDown(self):
        if os.path.exists(self.source_file):
            os.remove(self.source_file)
