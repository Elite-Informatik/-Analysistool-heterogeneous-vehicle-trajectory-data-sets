import os
import shutil
import unittest

from src.file.file.file_structure import FileStructure


class TestMoveFileFileFacade(unittest.TestCase):
    def setUp(self):
        self._file_facade = FileStructure()
        self.source_file = os.path.join(os.getcwd(), 'source_file.txt')
        self.destination_file = os.path.join(os.getcwd(), 'destination_file.txt')
        self.test_string = "testend"
        with open(self.source_file, 'w') as f:
            f.write(self.test_string)

    def test_move_file(self):
        # Test moving a file to a new location
        self._file_facade.move_file(self.source_file, self.destination_file)
        self.assertTrue(os.path.exists(self.source_file))
        self.assertTrue(os.path.exists(self.destination_file))

        with open(self.destination_file, "r") as f:
            self.assertEqual(self.test_string, f.read())

    def test_move_file_overwrite(self):
        # Test overwriting an existing file
        shutil.copy(self.source_file, self.destination_file)
        self._file_facade.move_file(self.source_file, self.destination_file)
        self.assertTrue(os.path.exists(self.source_file))
        self.assertTrue(os.path.exists(self.destination_file))

        with open(self.destination_file, "r") as f:
            self.assertEqual(self.test_string, f.read())

    def test_move_file_invalid_source(self):
        # Test moving a file with an invalid source path
        source_file = 'path/to/non_existent_file.txt'
        destination = 'path/to/destination_file.txt'

        with self.assertRaises(FileNotFoundError):
            self._file_facade.move_file(source_file, destination)

    def test_move_file_invalid_destination(self):
        # Test moving a file to an invalid destination path
        destination = 'path/to/non_existent_folder/destination_file.txt'

        with self.assertRaises(FileNotFoundError):
            self._file_facade.move_file(self.source_file, destination)

    def tearDown(self):
        if os.path.exists(self.source_file):
            os.remove(self.source_file)
        if os.path.exists(self.destination_file):
            os.remove(self.destination_file)
