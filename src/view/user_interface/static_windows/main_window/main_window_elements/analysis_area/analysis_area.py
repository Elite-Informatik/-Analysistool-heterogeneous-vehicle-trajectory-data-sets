import tkinter as tk
from tkinter import messagebox
from typing import List
from uuid import UUID

from src.controller.output_handling.event import AnalysisAdded, AnalysisImported
from src.controller.output_handling.event import AnalysisChanged
from src.controller.output_handling.event import AnalysisDeleted
from src.controller.output_handling.event import AnalysisRefreshed
from src.data_transfer.record import AnalysisDataRecord
from src.data_transfer.record import AnalysisRecord
from src.data_transfer.record.setting_record import SettingRecord
from src.view.controller_communication.controller_communication import ControllerCommunication
from src.view.data_request.data_request import DataRequest
from src.view.event_handler.event_consumers import AnalysisEventConsumer
from src.view.event_handler.i_event_hanlder_subscribe import IEventHandlerSubscribe
from src.view.user_interface.dialogs.create_analysis import CreateAnalysisDialog
from src.view.user_interface.dialogs.export_analysis import ExportAnalysisDialog
from src.view.user_interface.dialogs.import_analysis import ImportAnalysisDialog
from src.view.user_interface.selection.selection_window import SelectionWindow
from src.view.user_interface.static_windows.main_window.main_window_elements.analysis_area.analysis_notebook import \
    AnalysisNotebook
from src.view.user_interface.static_windows.main_window.main_window_elements.analysis_area.analysis_view_factory \
    import AnalysisViewFactory
from src.view.user_interface.static_windows.ui_element import UiElement
from src.view.user_interface.ui_util.texts import EnglishTexts


class AnalysisArea(UiElement, AnalysisEventConsumer):
    """
    This UI Element represents the analysis area to create and manage analysis views
    """

    def __init__(self,
                 controller_communication: ControllerCommunication,
                 data_request: DataRequest,
                 event_handler: IEventHandlerSubscribe):
        super().__init__(controller_communication, data_request, event_handler)

        self._notebook = AnalysisNotebook()
        self._change_menu: SelectionWindow = None
        self._current_analysis_id: UUID = None
        self._analysis_view_factory = AnalysisViewFactory()
        self._event_handler.subscribe_analysis_events(self)

    def build(self, master: tk.Widget) -> tk.Widget:
        """
        Build a new tk widget with a given tk.Widget
        :param master: the widget that the new widget is built in
        """
        self._base_frame = tk.Frame(master=master, height=500, width=500)
        menu_bar = self.__create_upper_menu_bar(self._base_frame)
        menu_bar.grid(row=0, sticky="ne")
        self._notebook_widget = self._notebook.build(self._base_frame)
        self._notebook_widget.grid(row=1, sticky="nsew")
        bottom_menu_bar = self.__create_bottom_menu_bar(self._base_frame)
        bottom_menu_bar.grid(row=2, sticky="ne")
        self._base_frame.columnconfigure(0, weight=1)
        self._base_frame.rowconfigure(0, weight=0)
        self._base_frame.rowconfigure(1, weight=1)
        return self._base_frame

    def destroy(self):
        self._base_frame.destroy()
        self._base_frame = None

    def __create_upper_menu_bar(self, master) -> tk.Frame:
        """
        builds the menu bar containing buttons
        :param master:  the master
        :return:        the frame containing the menu bar
        """
        menu_bar = tk.Frame(master)
        create_analysis_btn = tk.Button(master=menu_bar, text=EnglishTexts.CREATE_ANALYSIS_BTN_NAME.value,
                                        command=self.__on_create_analysis_button)
        create_analysis_btn.grid(row=0, column=0, sticky="ne")
        import_analysis_btn = tk.Button(master=menu_bar, text=EnglishTexts.IMPORT_ANALYSIS_BTN_NAME.value,
                                        command=self.__on_import_analysis_button)
        import_analysis_btn.grid(row=0, column=5, sticky="ne")
        return menu_bar

    def __create_bottom_menu_bar(self, master) -> tk.Frame:
        """
        builds the menu bar containing buttons
        :param master:  the master
        :return:        the frame containing the menu bar
        """
        menu_bar = tk.Frame(master)
        export_analysis_btn = tk.Button(master=menu_bar, text=EnglishTexts.EXPORT_ANALYSIS_BTN_NAME.value,
                                        command=self.__on_export_analysis_button)
        export_analysis_btn.grid(row=0, column=1, sticky="ne")
        refresh_analysis_btn = tk.Button(master=menu_bar, text=EnglishTexts.REFRESH_ANALYSIS_BTN_NAME.value,
                                         command=self.__on_refresh_button)
        refresh_analysis_btn.grid(row=0, column=2, sticky="ne")
        delete_analysis_btn = tk.Button(master=menu_bar, text=EnglishTexts.DELETE_ANALYSIS_BTN_NAME.value,
                                        command=self.__on_delete_button)
        delete_analysis_btn.grid(row=0, column=3, sticky="ne")
        change_analysis_btn = tk.Button(master=menu_bar, text=EnglishTexts.CHANGE_ANALYSIS_BTN_NAME.value,
                                        command=self.__on_change_analysis_button)
        change_analysis_btn.grid(row=0, column=4, sticky="ne")
        return menu_bar

    def process_added_analysis(self, event: AnalysisAdded):
        """
        Processes a added analysis event:
        :param event: the event that holds the added analysis
        """
        self.add_analysis(event.id)

    def process_imported_analysis(self, event: AnalysisImported):
        """
        processes a imported analysis event
        :param event: event that holds the imported analysis type
        """
        if self._base_frame is not None:
            messagebox.showinfo(title="Analysis Import", message="Import successful!")

    def process_deleted_analysis(self, event: AnalysisDeleted):
        """Processes a deleted analysis event:
        :param event: the event that holds the deleted analysis
        """
        self.delete_analysis(event.id)

    def process_refreshed_analysis(self, event: AnalysisRefreshed):
        """
        Updates the analyses based on a refreshed event
        :param event: the refreshed event
        """
        self.refresh(event.id)

    def process_changed_analysis(self, event: AnalysisChanged):
        """
        updates changed analyses
        :param event: the event that holds the changed analysis
        """
        self.refresh(event.id)

    def add_analysis(self, analysis_id: UUID):
        """
        adds a new analysis view
        :param analysis_id:     the id of the analysis to add
        """
        analysis_data: AnalysisDataRecord = self._data_request.get_analysis_data(analysis_id)
        self._notebook.add_analysis(analysis_data, analysis_id)

    def refresh(self, analysis_id: UUID):
        """
        refreshes the analysis view of the analysis with the given id
        :param analysis_id:     the analysis id
        """
        analyzed_data = self._data_request.get_analysis_data(analysis_id)
        self._notebook.refresh_analysis(analysis_id, analyzed_data)

    def delete_analysis(self, analysis_id: UUID):
        """
        deletes the analysis view of the analysis with the given id
        :param analysis_id:     the analysis id
        """
        self._notebook.delete_analysis(analysis_id)

    def __on_create_analysis_button(self):
        """
        executed when the create analysis button was pressed
        """
        dialog = CreateAnalysisDialog(self._data_request.get_analysis_types())
        if not dialog.valid_input:
            return
        selected_analysis = dialog.selected_analysis_type
        self._controller_communication.add_analysis(selected_analysis)

    def __on_export_analysis_button(self):
        """
        executed when the export analysis button was pressed
        """
        current_analysis = self._notebook.get_current_analysis_view()
        if current_analysis is None:
            return
        dialog = ExportAnalysisDialog(current_analysis.get_available_export_formats())
        if not dialog.valid_input:
            return
        selected_path = dialog.selected_path
        selected_export_format = dialog.selected_export_format
        selected_file_name = dialog.selected_file_name
        file = current_analysis.export(selected_export_format, selected_file_name)
        self._controller_communication.export_file(file, selected_path)

    def __on_refresh_button(self):
        """
        executed when the refresh analysis button was pressed
        """
        current_analysis = self._notebook.get_current_analysis_view()
        if current_analysis is None:
            return
        analysis_id = current_analysis.id
        self._controller_communication.refresh_analysis(analysis_id)

    def __on_delete_button(self):
        """
        executed when the delete analysis button was pressed
        """
        current_analysis = self._notebook.get_current_analysis_view()
        if current_analysis is None:
            return
        analysis_id = current_analysis.id
        self._controller_communication.delete_analysis(analysis_id)

    def __on_change_analysis_button(self):
        """
        executed when the change analysis button was pressed
        """
        current_analysis = self._notebook.get_current_analysis_view()
        if current_analysis is None:
            return
        self._current_analysis_id = current_analysis.id
        analysis_settings = self._data_request.get_analysis_settings(self._current_analysis_id)
        self._change_menu = SelectionWindow(analysis_settings.required_data, self.__on_change_confirm,
                                            EnglishTexts.CHANGE_ANALYSIS_DIALOG_TITLE.value)
        self._change_menu.run()

    def __on_change_confirm(self):
        """
        executed when user confirms changes on the analysis
        """
        new_analysis_settings: List[SettingRecord] = self._change_menu.new_setting_records
        self._controller_communication.change_analysis(self._current_analysis_id,
                                                       AnalysisRecord(tuple(new_analysis_settings)))

    def __on_import_analysis_button(self):
        """
        executed when the import analysis button was pressed
        """
        dialog = ImportAnalysisDialog()
        if not dialog.valid_input:
            return
        selected_path = dialog.selected_path
        self._controller_communication.import_analysis_type(selected_path)

    def destroy(self):
        if self._base_frame is not None:
            self._base_frame.destroy()
