import os.path
from unittest import TestCase
from src.file.file.importer.doc_importer import DocImporter


class TestDocImporter(TestCase):

    def test_fits_file_format(self):
        self.assertTrue(DocImporter().fits_file_format('file.doc'))
        self.assertFalse(DocImporter().fits_file_format('file.txt'))
        self.assertFalse(DocImporter().fits_file_format('file.docx'))
        self.assertFalse(DocImporter().fits_file_format('file.pdf'))
        self.assertFalse(DocImporter().fits_file_format('file.csv'))

    def test_import_data(self):
        """
        Uses the doc file in the test data folder to test the import.
        """
        doc_importer = DocImporter()
        # get the current directory
        current_dir = os.path.dirname(os.path.realpath(__file__))
        # get the parent directory
        parent_dir = os.path.dirname(current_dir)
        # get the path to the test data folder
        test_data_dir = os.path.join(parent_dir, 'data_for_tests')
        # get the path to the test doc file
        test_doc_dir = os.path.join(test_data_dir, 'SimraDaten')
        test_doc_file = os.path.join(test_doc_dir, 'VM2_-32876717')
        test_empty_doc_file = os.path.join(test_data_dir, 'VM2_1947534984#31')
        # import the data
        imported_data = doc_importer.import_data(test_doc_file)
        print(imported_data.data)
        self.assertNotEqual(imported_data.data.to_dict(), dict())

    def test_empty_import(self):
        doc_importer = DocImporter()
        # get the current directory
        current_dir = os.path.dirname(os.path.realpath(__file__))
        # get the parent directory
        parent_dir = os.path.dirname(current_dir)
        # get the path to the test data folder
        test_data_dir = os.path.join(parent_dir, 'data_for_tests')
        # get the path to the test doc file
        test_empty_doc_file = os.path.join(test_data_dir, 'VM2_1947534984#31')
        # import the data
        imported_data = doc_importer.import_data(test_empty_doc_file)
        self.assertEqual(imported_data.data.to_dict(), dict())
