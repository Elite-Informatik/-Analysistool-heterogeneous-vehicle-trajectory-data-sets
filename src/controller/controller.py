from abc import ABC
from abc import abstractmethod

from src.controller.execution_handling.analysis_manager import AnalysisManager
from src.controller.execution_handling.database_manager import DatabaseManager
from src.controller.execution_handling.export_manager import ExportManager
from src.controller.execution_handling.filter_manager.filter_manager import FilterManager
from src.controller.execution_handling.filter_manager.filterer import Filterer
from src.controller.execution_handling.polygon_manager import PolygonManager
from src.controller.execution_handling.setting_manager import SettingManager
from src.controller.input_handling.application_manager import ApplicationManager
from src.controller.input_handling.command_input import CommandInput
from src.controller.input_handling.commands.command_factory import CommandFactory
from src.controller.input_handling.commands.command_manager import CommandManager
from src.controller.input_handling.request_distributor import RequestDistributor
from src.controller.output_handling.event_manager import EventManager
from src.controller.output_handling.request_manager import InputRequestManager
from src.database.idatabase import IDatabase
from src.file.file_facade import FileFacade
from src.model.imodel import IModel
from src.view.iview import IView


class IController(ABC):
    """
    this interface represents the controller
    """

    @property
    @abstractmethod
    def data_request_facade(self):
        """
        Getter-Method for the data request facade of the controller

        :return: the current data request facade of the controller
        """
        pass

    @property
    @abstractmethod
    def communication_facade(self):
        """
        Getter-Method for the communication facade of the controller

        :return: the current communication facade of the controller
        """
        pass


class Controller(IController):
    """
    represents the controller
    """

    def __init__(self):
        """
        Initialize the controller. Constructor that starts all managers and factories. Furthermore, it
        subscribes to the different component.
        """
        self._analysis_facade_consumers = list()
        self._data_facade_consumers = list()
        self._dataset_facade_consumers = list()
        self._event_handler_consumers = list()
        self._file_facade_consumers = list()
        self._filter_facade_consumers = list()
        self._polygon_facade_consumers = list()
        self._setting_facade_consumers = list()
        self._user_input_facade_consumers = list()
        self._execution_component_consumer = list()

        self._abstract_managers = list()
        self._execution_component_consumer = list()

        self._database = None
        self._view = None
        self._model = None
        self._file_adapter = None

        command_manager = CommandManager()

        event_manager = EventManager()
        self._event_handler_consumers.append(event_manager)

        request_manager = InputRequestManager()
        self._user_input_facade_consumers.append(request_manager)

        filter_manager = FilterManager()
        self._filter_facade_consumers.append(filter_manager)
        self._data_facade_consumers.append(filter_manager)
        self._setting_facade_consumers.append(filter_manager)
        self._abstract_managers.append(filter_manager)

        analysis_manager = AnalysisManager()
        self._analysis_facade_consumers.append(analysis_manager)
        self._file_facade_consumers.append(analysis_manager)
        self._abstract_managers.append(analysis_manager)

        database_manager = DatabaseManager()
        self._file_facade_consumers.append(database_manager)
        self._dataset_facade_consumers.append(database_manager)
        self._data_facade_consumers.append(database_manager)
        self._abstract_managers.append(database_manager)

        export_manager = ExportManager()
        self._file_facade_consumers.append(export_manager)
        self._data_facade_consumers.append(export_manager)
        self._abstract_managers.append(export_manager)

        setting_manager = SettingManager()
        self._setting_facade_consumers.append(setting_manager)
        self._file_facade_consumers.append(setting_manager)
        self._abstract_managers.append(setting_manager)

        polygon_manager = PolygonManager()
        self._polygon_facade_consumers.append(polygon_manager)
        self._abstract_managers.append(polygon_manager)

        filterer = Filterer()
        self._data_facade_consumers.append(filterer)
        self._dataset_facade_consumers.append(filterer)
        self._setting_facade_consumers.append(filterer)
        self._abstract_managers.append(filterer)

        for manager in self._abstract_managers:
            manager.set_event_manager(event_manager)
            manager.set_request_manager(request_manager)

        self._data_request = RequestDistributor()
        self._data_request.set_getter(setting_manager,
                                      polygon_manager,
                                      database_manager,
                                      filter_manager,
                                      analysis_manager,
                                      filterer)

        self._file_facade_consumers.append(self._data_request)

        application_manager = ApplicationManager(analysis_manager=analysis_manager,
                                                 setting_manager=setting_manager,
                                                 dataset_manager=database_manager)
        self._execution_component_consumer.append(application_manager)

        self._application_command_facade: ApplicationManager = application_manager

        self._communication: CommandInput = CommandInput()
        self._communication.set_factory(CommandFactory(analysis_manager=analysis_manager,
                                                       analysis_getter=analysis_manager,
                                                       setting_manager=setting_manager,
                                                       setting_getter=setting_manager,
                                                       database_manager=database_manager,
                                                       filter_manager=filter_manager,
                                                       filter_getter=filter_manager,
                                                       polygon_manager=polygon_manager,
                                                       command_manager=command_manager,
                                                       export_manager=export_manager))

        self._communication.set_command_handler(command_manager)
        self._communication.set_application_manager(application_manager)

        # Responsible for correct Application start

    def set_view(self, view: IView):
        """
        Setter method for the view attribute of the controller
        :param view: the new view of the controller
        """
        self._view = view
        for event_handler_consumer in self._event_handler_consumers:
            event_handler_consumer.subscribe(view.event_handler())

        for user_input_request_consumer in self._user_input_facade_consumers:
            user_input_request_consumer.set_user_input_request_facade(view.user_input_request())

        for execution_component_consumer in self._execution_component_consumer:
            execution_component_consumer.add_execution_components(view)

    def set_database(self, database: IDatabase):
        """
        Setter method for the database attribute of the controller

        :param database: the new database of the controller
        """
        self._database = database
        for data_facade_consumer in self._data_facade_consumers:
            data_facade_consumer.set_data_facade(database.database_facade)

        for dataset_facade_consumer in self._dataset_facade_consumers:
            dataset_facade_consumer.set_dataset_facade(database.database_facade)

    def set_model(self, model: IModel):
        """
        Setter method for the model attribute of the controller

        :param model: the new model of the controller
        """
        self._model = model
        for analysis_facade_consumer in self._analysis_facade_consumers:
            analysis_facade_consumer.set_analysis_facade(model.model_facade)

        for filter_facade_consumer in self._filter_facade_consumers:
            filter_facade_consumer.set_filter_facade(model.model_facade)

        for polygon_facade_consumer in self._polygon_facade_consumers:
            polygon_facade_consumer.set_polygon_facade(model.model_facade)

        for setting_facade_consumer in self._setting_facade_consumers:
            setting_facade_consumer.set_setting_facade(model.model_facade)

    def set_file(self, file_facade: FileFacade):
        """
        Setter method for the file_adapter attribute of the controller

        :param file_facade: the new file model_manager of the controller
        """

        for file_manager_consumer in self._file_facade_consumers:
            file_manager_consumer.set_file_facade(file_facade)

    @property
    def data_request_facade(self):
        """
        Returns the data request facade
        """
        return self._data_request

    @property
    def communication_facade(self):
        """
        Returns the communication facade
        """
        return self._communication

    @property
    def application_command_facade(self):
        """
        Returns the application facade
        """
        return self._application_command_facade
