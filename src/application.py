from typing import List

from src.controller.application_facade import ApplicationFacade
from src.controller.controller import Controller
from src.data_transfer.content.text_provider import TextProvider
from src.database import Database
from src.executable_component import ExecutableComponent
from src.file.file_facade_manager import FileFacadeManager
from src.model.model import Model
from src.view.view import View


class Application(ApplicationFacade):
    """
    The Application is the main class of the application.
    """
    _executable_components: List[ExecutableComponent]

    def __init__(self):
        # create all components of the program
        TextProvider.create('eng')
        file_adapter = FileFacadeManager()
        controller = Controller()
        database = Database()
        model = Model()
        view = View()

        # Establish Relationships between Components
        controller.set_model(model)
        controller.set_view(view)
        controller.set_database(database)
        controller.set_file(file_adapter)
        view.set_controller(controller)
        model.set_controller(controller)

        # Add executable Components to list
        self._application_command_facade = controller.application_command_facade

    def start(self):
        """
        Start the application. Starts the components of the application in starting order.
        """
        self._application_command_facade.start()

    def stop(self):
        """
        Stops the application. Stops the components of the application in reversed starting order
        """
        self._application_command_facade.stop()


if __name__ == "__main__":
    """
    the entry point of the application
    """
    application = Application()
    application.start()
    application.stop()
