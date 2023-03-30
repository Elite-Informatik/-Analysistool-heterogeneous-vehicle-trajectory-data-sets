# todo: mehr namen
import os

from test.controller.test_command import StartedStoppedControllerTest, DatasetAdded, DatasetOpened

names_wrong = []
names_right = ["aa", "aaaa", "aa_aa", "b"] + ["1", "2", "'", "#", "123ue09853092küegfsd"]


class WrongDataSetNamesTest(StartedStoppedControllerTest):
    def setUp(self) -> None:
        super().setUp()
        self.current_dir = os.getcwd()
        os.chdir(os.path.join(os.path.dirname(self.current_dir), 'test'))

    def tearDown(self) -> None:
        os.chdir(self.current_dir)
        super().tearDown()

    def test_wrong_dataset_names(self):
        for name in names_wrong:
            self.controller.communication_facade.import_dataset(
                ["file/example_data_generated/intern_data4.csv"],
                name, "intern"
            )
            self.check_errors([f"The name of the dataset is invalid Dataset name '{name}' is not valid! at importing "
                               f"dataset in manager"])
            self.errors.pop()

    def test_write_dataset_names(self):
        for name in names_right:
            self.open_dataset_intern(path="file/example_data_generated/intern_data4.csv", name=name)





