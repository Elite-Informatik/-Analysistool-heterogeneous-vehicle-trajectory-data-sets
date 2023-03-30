import tkinter as tk
import tkinter.messagebox as messagebox
from typing import Dict
from uuid import UUID

from tktooltip import ToolTip

from src.controller.output_handling.event import DatasetAdded
from src.controller.output_handling.event import DatasetDeleted
from src.controller.output_handling.event import DatasetOpened
from src.data_transfer.record import DatasetRecord
from src.view.controller_communication.controller_communication import ControllerCommunication
from src.view.data_request.data_request import DataRequest
from src.view.event_handler.event_consumers.dataset_event_consumer import DatasetEventConsumer
from src.view.event_handler.event_handler import IEventHandlerSubscribe
from src.view.user_interface.dialogs.import_dataset import ImportDatasetDialog
from src.view.user_interface.dialogs.open_dataset import OpenDatasetDialog
from src.view.user_interface.gui import GUI
from src.view.user_interface.static_windows.ui_element import UiElement
from src.view.user_interface.ui_util.texts import EnglishTexts


class StartWindowBaseFrame(UiElement, DatasetEventConsumer):
    """
    Implements the Base Frame of the start window.
    The Class implements the DatasetEventConsumer interface. Thereby the start window base frame
    is able to process dataset events.
    """

    def __init__(self, controller_communication: ControllerCommunication, data_request: DataRequest,
                 event_handler: IEventHandlerSubscribe):
        """
        Creates a new StartWindowBaseFrame and subscribes it to the Event Handler.
        The start window base frame keeps track of the datasets.
        """
        super().__init__(controller_communication, data_request, event_handler)

        self._choose_label = None
        self._import_button = None
        self._open_button = None
        self._event_handler.subscribe_dataset_events(self)
        self._datasets: Dict[UUID, DatasetRecord] = {}

    def build(self, master: tk.Widget) -> tk.Widget:
        """
        See documentation of the UiElement class.
        """
        self._base_frame = tk.Frame(master=master)

        self._choose_label = tk.Label(master=self._base_frame, text=EnglishTexts.START_WINDOW_QUESTION.value,
                                      font=("Arial", 12))
        self._import_button = tk.Button(master=self._base_frame,
                                        text="import dataset",
                                        command=self.on_import_button)
        self._open_button = tk.Button(master=self._base_frame,
                                      text="open dataset",
                                      command=self.on_open_button)
        self._choose_label.grid(column=0, row=0, sticky="NSEW", pady=20)
        self._import_button.grid(column=0, row=2, sticky="NSEW", pady=3)
        self._open_button.grid(column=0, row=3, sticky="NSEW", pady=3)

        ToolTip(widget=self._import_button, msg=EnglishTexts.IMPORT_DATASET_TIP.value, delay=0.2)
        ToolTip(widget=self._open_button, msg=EnglishTexts.OPEN_DATASET_TIP.value, delay=0.2)

        return self._base_frame

    def destroy(self):
        """
        See documentation of the UiElement class
        """
        self._base_frame.destroy()
        self._base_frame = None

    def on_import_button(self):
        """
        Handler for the import button press. A new dialog will be opened in which the user
        can select the dataset file that should be imported.
        """
        formats = self._data_request.get_data_formats()
        dialog = ImportDatasetDialog(data_formats=formats)
        if not dialog.is_valid():
            return

        paths = dialog.get_paths()
        name = dialog.get_name()
        dataset_format = dialog.get_format()
        self._controller_communication.import_dataset(paths, name, dataset_format)

    def on_open_button(self):
        """
        Handler for the open button press. A new dialog will be opened in which the user can select
        one of the existing datasets to initialize the application with.
        """
        if len(self._datasets) == 0:
            messagebox.showinfo(message=EnglishTexts.NO_DATASET_IMPORTED_YET.value)
            return

        dialog = OpenDatasetDialog(datasets=self._datasets)
        if not dialog.is_valid():
            return

        selected_id = dialog.get_id_selected()
        self._controller_communication.open_dataset(uuid=selected_id)

    def process_added_dataset(self, event: DatasetAdded):
        """
        Adds a new dataset to the list. All operations on datasets should now include the new dataset.
        """
        dataset_id = event.id
        new_dataset = self._data_request.get_dataset_meta(event.id)
        self._datasets[dataset_id] = new_dataset

    def process_deleted_dataset(self, event: DatasetDeleted):
        """
        Deletes a dataset. The deleted dataset wont be shown in any further dialogs.
        """
        self._datasets.pop(event.id)

    def process_opened_dataset(self, event: DatasetOpened):
        """
        When a dataset got opened the Base Frame tells the GUI to switch to the main window.
        """
        GUI.switch_to_main_window()
