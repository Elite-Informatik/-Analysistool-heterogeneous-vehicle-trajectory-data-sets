import os

from src.data_transfer.content import Column
from src.data_transfer.record import DataRecord
from test.controller.test_command import StartedStoppedControllerTest


class SimraImportTest(StartedStoppedControllerTest):

    def setUp(self) -> None:
        test_path: str = os.path.dirname(os.path.realpath(__file__))
        test_path = os.path.split(test_path)[0]
        os.chdir(test_path)
        super().setUp()
        self.current_dir = os.getcwd()
        os.chdir(os.path.join(os.path.dirname(self.current_dir), 'test'))

    def test_import(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        print(current_dir)
        # get the path to the test data folder
        test_data_dir = os.path.join(current_dir, 'data_for_tests')
        test_simra_dir = os.path.join(test_data_dir, 'SimraDaten')

        self.open_dataset_simra_bicycle(test_simra_dir)
        data: DataRecord = self.controller.data_request_facade.get_rawdata(Column.list())
        self.assertGreater(len(data.data), 0)
        print("Imported data:", data.data)