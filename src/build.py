import json
import os

from src.controller.execution_handling.analysis_manager import AnalysisManager
from src.controller.execution_handling.database_manager import DatabaseManager
from src.controller.execution_handling.setting_manager import SettingManager
from src.controller.input_handling.application_manager import ApplicationManager
from src.database import Database
from src.database.dataset_facade import DatasetFacade
from src.file.file_facade_manager import FileFacadeManager
from src.model.model_facade import ModelFacade
from src.model.setting_structure.setting_structure import SettingStructure


def set_sql_connection():
    """
    """
    d = {
        "database": "Analysistool",
        "user": "analysisUser",
        "password": "1234",
        "host": "localhost",
        "port": "5432"
    }
    f = FileFacadeManager()
    f.set_standard_paths("model/analysis_structure/concrete_analysis", "dictionary")
    f.export_dictionary_to_standard_path("sql_connection", d)


if __name__ == "__main__":
    cwd = os.getcwd()

    if os.path.isdir(os.path.join(cwd, "dictionary")):
        pass
    else:
        os.makedirs(os.path.join(cwd, "dictionary"))

    # settings generator
    setting = SettingManager()
    model = ModelFacade()
    file = FileFacadeManager()
    model.set_setting_structure(SettingStructure())
    setting.set_setting_facade(model)
    setting.set_file_facade(file)
    data = DatabaseManager()
    data.set_file_facade(file)
    app = ApplicationManager(AnalysisManager(), setting, data)
    app.set_file_facade(file)
    app.set_paths()
    app.save_settings()

    # datasets generator
    setting = SettingManager()
    model = ModelFacade()
    file = FileFacadeManager()
    model.set_setting_structure(SettingStructure())
    setting.set_setting_facade(model)
    setting.set_file_facade(file)
    data = DatabaseManager()
    data.set_file_facade(file)

    dataset_facade: DatasetFacade = Database()
    data.set_dataset_facade(dataset_facade=dataset_facade)
    app = ApplicationManager(AnalysisManager(), setting, data)
    app.set_file_facade(file)

    app.set_dataset_facade(dataset_facade=dataset_facade)
    app.set_paths()
    app.save_datasets()

    with open(cwd + "/dictionary/datasets.json") as file:
        dict = json.load(file)
        json_object = json.dumps(dict)

    # Writing to sample.json
    with open(cwd + "/dictionary/datasets.json", "w") as outfile:
        outfile.write(json_object)

    set_sql_connection()
