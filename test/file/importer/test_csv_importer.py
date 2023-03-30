import os
import re
from unittest import TestCase

import pandas as pd
from pandas.testing import assert_frame_equal

from src.file.file.importer.csv_importer import CSVImporter


class TestCSVImporter(TestCase):
    def setUp(self):
        self.source_file = os.path.join(os.getcwd(), 'test_file.csv')
        self.test_data = {'col1': [1, 2, 3], 'col2': [4, 5, 6]}
        self.test_df = pd.DataFrame(self.test_data)
        self.test_df.to_csv(self.source_file, index=False, sep=",")

    def test_fits_file_format(self):
        csv_importer = CSVImporter()
        self.assertTrue(re.search(csv_importer.file_format, 'file.csv'))
        self.assertFalse(re.search(csv_importer.file_format, 'file.json'))
        self.assertTrue(csv_importer.fits_file_format('file.csv'))
        self.assertFalse(csv_importer.fits_file_format('file.txt'))

    def test_import_data(self):
        csv_importer = CSVImporter()
        imported_data = csv_importer.import_data(self.source_file)
        assert_frame_equal(self.test_df, imported_data.data)

    def test_import_data_raises_file_not_found_error(self):
        csv_importer = CSVImporter()
        with self.assertRaises(FileNotFoundError):
            csv_importer.import_data('path/to/non_existent_file.csv')

    def tearDown(self):
        if os.path.exists(self.source_file):
            os.remove(self.source_file)
