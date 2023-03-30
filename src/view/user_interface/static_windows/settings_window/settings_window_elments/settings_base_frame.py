import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror
from typing import List

from src.controller.output_handling.event import SettingsChanged
from src.data_transfer.record import SettingsRecord
from src.view.controller_communication.controller_communication import ControllerCommunication
from src.view.data_request.data_request import DataRequest
from src.view.event_handler import IEventHandlerSubscribe
from src.view.event_handler.event_consumers import SettingsEventConsumer
from src.view.user_interface.gui import GUI
from src.view.user_interface.static_windows.settings_window.settings_window_elments.settings_page import SettingsPage
from src.view.user_interface.static_windows.settings_window.settings_window_factory import SettingsWindowFactory
from src.view.user_interface.static_windows.ui_element import UiElement
from src.view.user_interface.ui_util.texts import EnglishTexts


class SettingsBaseFrame(UiElement, SettingsEventConsumer):
    """
    The base frame of the settings window.
    The settings window processes the settings events.
    """

    def __init__(self, controller_communication: ControllerCommunication, data_request: DataRequest,
                 event_handler: IEventHandlerSubscribe, factory: SettingsWindowFactory):
        super().__init__(controller_communication, data_request, event_handler)

        self._settings_notebook = None
        self._settings = None
        self._button_row = None
        self._button_ok = None
        self._button_apply = None
        self._button_cancel = None
        self._event_handler = event_handler
        self._event_handler.subscribe_settings_events(self)
        self._factory = factory

        self._pages: List[SettingsPage] = []

    def build(self, master: tk.Widget) -> tk.Widget:
        """
        See documentation of the UiElement class.
        """
        self._base_frame = tk.Frame(master=master)

        self._settings_notebook = ttk.Notebook(master=self._base_frame)
        # settings are requested with every build so temporary changes in the view are reset
        self._settings = self._data_request.get_settings()
        for page in self._settings.pages:
            view_page_unbuild = self._factory.create_settings_page(page)
            self._pages.append(view_page_unbuild)

            view_page = view_page_unbuild.build(master=self._settings_notebook)
            self._settings_notebook.add(view_page, text=page.name)

        self._settings_notebook.grid(column=0, row=0, sticky="nsew")

        self._button_row = tk.Frame(master=self._base_frame)
        self._button_ok = tk.Button(master=self._button_row, text="Ok", command=self.ok)
        self._button_apply = tk.Button(master=self._button_row, text="Apply", command=self.apply_settings)
        self._button_cancel = tk.Button(master=self._button_row, text="Cancel", command=self.cancel)
        self._button_ok.grid(column=0, row=0, sticky="nsew")
        self._button_apply.grid(column=1, row=0, sticky="nsew")
        self._button_cancel.grid(column=2, row=0, sticky="nsew")
        self._button_row.grid(column=0, row=1, sticky="sw")

        return self._base_frame

    def destroy(self):
        """
        See documentation of the UiElement class.
        """
        for page in self._pages:
            page.destroy()
        self._pages = []

    def process_changed_settings(self, event: SettingsChanged):
        """
        The settings changed event is not processed, because all changes to the settings are done in this window
        and thereby do not need to be refreshed again.
        """
        pass

    def apply_settings(self) -> bool:
        """
        Executed when the apply button is pressed.
        This method validates the input. If the input is valid the
        settings are applied by sending them to the controller.
        :return: True if the settings were applied, False if the settings were not applied because of invalid input.
        """
        if self.__validate():
            new_pages = []
            for page in self._pages:
                new_pages.append(page.to_page())
            new_settings = SettingsRecord(_pages=tuple(new_pages))
            self._controller_communication.change_settings(settings=new_settings)
            return True
        else:
            showerror(message=EnglishTexts.ERROR_INVALID_INPUT.value,
                      title=EnglishTexts.INSTRUCTION_INVALID_INPUT.value)
            return False

    def __validate(self) -> bool:
        """
        Validates the input of all pages.
        :return: True if the input is valid, False if the input is invalid.
        """
        for page in self._pages:
            if not page.validate():
                return False
        return True

    def ok(self):
        """
        executed when the ok button is pressed.
        This methods is the same than the apply method, except that the settings window is closed afterwards.
        """
        self.apply_settings()
        GUI.close_settings_window()

    def cancel(self):
        """
        executed when the cancel button is pressed.
        Closes the settings window without the changes being applied.
        """
        GUI.close_settings_window()
