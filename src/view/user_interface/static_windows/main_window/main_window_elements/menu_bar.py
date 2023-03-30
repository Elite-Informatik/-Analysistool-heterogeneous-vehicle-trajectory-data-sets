import tkinter as tk

from src.view.controller_communication.controller_communication import ControllerCommunication
from src.view.data_request.data_request import DataRequest
from src.view.event_handler import IEventHandlerSubscribe
from src.view.user_interface.dialogs import ImportDatasetDialog
from src.view.user_interface.dialogs.export_dataset import ExportDatasetDialog
from src.view.user_interface.gui import GUI
from src.view.user_interface.static_windows.ui_element import UiElement


class MenuBar(UiElement):
    """
    This menubar represents the menu bar at the top of the main window over which the user can navigate
    to the settings and import/ export datasets
    """

    def __init__(self,
                 controller_communication: ControllerCommunication,
                 data_request: DataRequest,
                 event_handler: IEventHandlerSubscribe):
        super().__init__(controller_communication, data_request, event_handler)
        self._file_menu = None
        self._settings_menu = None
        self._help_menu = None

    def build(self, master: tk.Widget) -> tk.Widget:
        """
        See documentation of the UiElement class.
        """
        self._base_frame = tk.Menu(master=master, tearoff=0)
        self._file_menu = tk.Menu(master=self._base_frame, tearoff=0)
        self._file_menu.add_command(label="import dataset", command=self.import_dataset)
        self._file_menu.add_command(label="export dataset", command=self.export_dataset)

        self._settings_menu = tk.Menu(master=self._base_frame, tearoff=0)
        self._settings_menu.add_command(label="datasets", command=self.dataset_manager)
        self._settings_menu.add_command(label="settings", command=self.open_settings)

        self._help_menu = tk.Menu(master=self._base_frame, tearoff=0)
        self._help_menu.add_command(label="open manual", command=self.open_manual)

        self._base_frame.add_cascade(label="File", menu=self._file_menu)
        self._base_frame.add_cascade(label="Settings", menu=self._settings_menu)
        self._base_frame.add_cascade(label="Help", menu=self._help_menu)
        return self._base_frame

    def destroy(self):
        """
        See documentation of the UiElement class.
        """
        self._base_frame.destroy()

    def import_dataset(self):
        """
        called when the user clicks the import dataset option in the menu bar
        """
        formats = self._data_request.get_data_formats()
        dialog = ImportDatasetDialog(data_formats=formats)
        if not dialog.is_valid():
            return
        paths = dialog.get_paths()
        name = dialog.get_name()
        dataset_format = dialog.get_format()
        self._controller_communication.import_dataset(paths, name, dataset_format)

    def export_dataset(self):
        """
        called when user wants to export a dataset
        """
        dialog = ExportDatasetDialog()
        if dialog.valid_input:
            path = dialog.selected_path
            self._controller_communication.export_dataset(path)

    def dataset_manager(self):
        """
        gets called when the user clicks the dataset manager option in the context menu
        """
        GUI.open_dataset_window()

    def open_settings(self):
        """
        gets called when the user clicks the settings option in the context menu
        """
        GUI.open_settings_window()

    def open_manual(self):
        GUI.open_manual_window()
