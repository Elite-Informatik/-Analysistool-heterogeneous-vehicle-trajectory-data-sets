from unittest import TestCase

from src.file.file.exporter.data_exporter import DataExporter


class TestUnpacker(TestCase):
    def test_unpack_abstract_class(self):
        with self.assertRaises(TypeError):
            data_exporter = DataExporter()
