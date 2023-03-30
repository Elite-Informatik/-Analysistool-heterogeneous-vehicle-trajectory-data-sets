import unittest

import pandas as pd

from src.file.converter.util.data_util import repair_number_column


class UtilTest(unittest.TestCase):
    number_data_frames: [pd.DataFrame] = [
        pd.DataFrame({'number': ["2", 0, None, 6, None, 4]}),
        pd.DataFrame({'number': ["0", None, None, None, None, 5, None]})
    ]
    expected_result_numbers = [
        [2.0, 0.0, 3.0, 6.0, 5.0, 4.0],
        [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 5.0]

    ]

    def test_repair_number_column(self):
        print()
        for expected_result, number_frame in zip(self.expected_result_numbers, self.number_data_frames):
            # repair_number_column(column_frame=number_frame['number'], def_value=0).to_list())
            print(repair_number_column(column_frame=number_frame['number'], def_value=0, con_val="number",
                                       linear_transition=True))


if __name__ == '__main__':
    unittest.main()
