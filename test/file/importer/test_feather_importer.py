import os
import re
from unittest import TestCase

import pandas as pd
from pandas.testing import assert_frame_equal

from src.file.file.importer.feather_importer import FeatherImporter


class TestFeatherImporter(TestCase):
    def setUp(self):
        self.source_file = os.path.join(os.getcwd(), 'test_file.feather')
        self.test_data = {'col1': [1, 2, 3], 'col2': [4, 5, 6]}
        self.test_df = pd.DataFrame(self.test_data)
        self.test_df.to_feather(self.source_file)

    def test_fits_file_format(self):
        feather_importer = FeatherImporter()
        self.assertTrue(re.search(feather_importer.file_format, 'file.feather'))
        self.assertFalse(re.search(feather_importer.file_format, 'file.csv'))
        self.assertTrue(feather_importer.fits_file_format('file.feather'))
        self.assertFalse(feather_importer.fits_file_format('file.txt'))

    def test_import_data(self):
        feather_importer = FeatherImporter()
        imported_data = feather_importer.import_data(self.source_file)
        assert_frame_equal(self.test_df, imported_data.data)

    def test_import_data_raises_file_not_found_error(self):
        feather_importer = FeatherImporter()
        with self.assertRaises(FileNotFoundError):
            feather_importer.import_data('path/to/non_existent_file.feather')

    def tearDown(self):
        if os.path.exists(self.source_file):
            os.remove(self.source_file)
