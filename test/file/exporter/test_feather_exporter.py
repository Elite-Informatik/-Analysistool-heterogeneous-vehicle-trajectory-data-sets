import os
from unittest import TestCase

from pandas import DataFrame

from src.file.file.exporter.feather_exporter import FeatherExporter


class TestFeatherExporter(TestCase):

    def setUp(self):
        self.source_file = os.path.join(os.getcwd(), 'test_file.feather')
        self.exporter = FeatherExporter()

    def test_get_file_format(self):
        self.assertEqual(self.exporter.get_file_format(), 'feather',
                         'Should get file format.')

    def test_export_data(self):
        test_data = DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        self.exporter.export_data(self.source_file, test_data)
        with open(self.source_file, 'rb') as file:
            lines = file.read().splitlines()
            self.assertGreaterEqual(len(lines), 4,
                                    'Should export data correctly.')

    def tearDown(self):
        if os.path.exists(self.source_file):
            os.remove(self.source_file)
