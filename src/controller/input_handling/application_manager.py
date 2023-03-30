import threading

from src.controller.application_facade import ApplicationFacade
from src.controller.execution_handling.analysis_manager import IAnalysisManager
from src.controller.execution_handling.database_manager import IDatabaseManager
from src.controller.execution_handling.setting_manager import ISettingManager
from src.controller.facade_consumer.analysis_facade_consumer import AnalysisFacadeConsumer
from src.controller.facade_consumer.dataset_facade_consumer import DatasetFacadeConsumer
from src.controller.facade_consumer.execution_component_consumer import ExecutionComponentConsumer
from src.controller.facade_consumer.file_facade_consumer import FileFacadeConsumer

from src.data_transfer.content.logger import ThreadLogger
from src.data_transfer.exception.custom_exception import StandardPathNotExisting

STANDARD_ANALYSIS_PATH = "model/analysis_structure/concrete_analysis"
STANDARD_DICTIONARY_PATH = "dictionary"
STANDARD_DATA_SET_DICT = "datasets"
STANDARD_SQL_CONNECTION = "sql_connection"
STANDARD_SETTING_DICT = "setting"


class ApplicationManager(ApplicationFacade, ExecutionComponentConsumer, FileFacadeConsumer,
                         AnalysisFacadeConsumer, DatasetFacadeConsumer):
    """
    represents a manager for starting and stopping the application
    """

    def __init__(self, analysis_manager: IAnalysisManager, setting_manager: ISettingManager,
                 dataset_manager: IDatabaseManager):
        """
        Constructor for a new application manager
        """
        super().__init__()
        self._analysis_manager = analysis_manager
        self._setting_manager = setting_manager
        self._dataset_manager = dataset_manager

    def start(self):
        """
        Loads different files and initializes the settings
        """
        self.set_paths()
        self.set_sql_connection()
        self.load_datasets()
        self.load_settings()
        self.load_analyses()

        application_thread = ThreadLogger(self.save)
        application_thread.start()
        self.run()

    def run(self):
        self._start_other_components()
        self.stop()

    def save(self):
        self.save_settings()
        self.save_datasets()

    def stop(self):
        """
        Stops the application and saves to files
        """
        self.save()

    def _start_other_components(self):
        """
        Starts the other components
        """
        self.application_execution_facade.start()

    def set_paths(self):
        """
        Sets the standard paths for the program
        """
        if not self._dataset_manager.set_standard_paths(STANDARD_DICTIONARY_PATH, STANDARD_ANALYSIS_PATH):
            raise StandardPathNotExisting("The standard path for the datasets is not existing")

    def set_sql_connection(self):
        """
        Sets the sql connection on start based on the standard path
        """
        if not self._dataset_manager.set_sql_connection(STANDARD_SQL_CONNECTION):
            raise StandardPathNotExisting("The standard path for the sql connection is not existing")

    def load_datasets(self):
        """
        Loads the saved datasets into the current state
        """
        self._dataset_manager.initialize_datasets(STANDARD_DATA_SET_DICT)

    def load_analyses(self):
        """
        Loads the imported analyses
        """
        self._analysis_manager.update_imported_analyses()

    def load_settings(self):
        """
        Laods the settings from the jason file
        """
        self._setting_manager.import_settings(STANDARD_SETTING_DICT)

    def save_settings(self):
        """
        Saves the setting sto the dict path to the json file
        """
        self._setting_manager.export_settings(STANDARD_SETTING_DICT)

    def save_datasets(self):
        """
        Saves the datasets to the standard path
        """
        self._dataset_manager.save_datasets(STANDARD_DATA_SET_DICT)
