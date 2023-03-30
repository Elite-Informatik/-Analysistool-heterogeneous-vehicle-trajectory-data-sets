from unittest import TestCase

from src.file.file.importer.data_importer import DataImporter


class TestUnpacker(TestCase):
    def test_unpack_abstract_class(self):
        with self.assertRaises(TypeError):
            data_importer = DataImporter()
