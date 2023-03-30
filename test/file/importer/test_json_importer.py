import os
import re
from unittest import TestCase

import pandas as pd
from pandas.testing import assert_frame_equal

from src.file.file.importer.json_importer import JSONImporter


class TestJSONImporter(TestCase):
    def setUp(self):
        self.source_file = os.path.join(os.getcwd(), 'test_file.json')
        self.test_data = {'col1': [1, 2, 3], 'col2': [4, 5, 6]}
        self.test_df = pd.DataFrame(self.test_data)
        self.test_df.to_json(self.source_file, orient='records')

    def test_fits_file_format(self):
        json_importer = JSONImporter()
        self.assertTrue(re.search(json_importer.file_format, 'file.json'))
        self.assertFalse(re.search(json_importer.file_format, 'file.csv'))
        self.assertTrue(json_importer.fits_file_format('file.json'))
        self.assertFalse(json_importer.fits_file_format('file.csv'))

    def test_import_data(self):
        json_importer = JSONImporter()
        imported_data = json_importer.import_data(self.source_file)
        assert_frame_equal(self.test_df, imported_data.data)

    def tearDown(self):
        if os.path.exists(self.source_file):
            os.remove(self.source_file)
