import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror
from tkinter.ttk import Notebook
from typing import List
from typing import Optional
from uuid import UUID

from src.data_transfer.record import AnalysisDataRecord
from src.data_transfer.record import FileRecord
from src.view.user_interface.static_windows.main_window.main_window_elements.analysis_area.analysis_view_factory \
    import AnalysisViewFactory
from src.view.user_interface.static_windows.main_window.main_window_elements.analysis_area.concrete_analyses. \
    analysis_view import AnalysisView
from src.view.user_interface.ui_util.texts import EnglishTexts


class AnalysisNotebook:
    """
    This class is responsible to manage the analysis view tabs
    """

    def __init__(self):
        self._notebook: Notebook = None
        self._analysis_views: List[AnalysisView] = []
        self._analysis_view_factory = AnalysisViewFactory()

    def build(self, master) -> tk.Widget:
        """
        builds the AnalysisNotebook
        :param master:  the master
        :return:        the widget containing the analysis notebook
        """
        self._notebook = ttk.Notebook(master=master, height=500, width=500)
        self._notebook.columnconfigure(0, weight=1)
        self._notebook.rowconfigure(0, weight=1)
        for analysis_view in self._analysis_views:
            analysis_tab = ttk.Frame(self._notebook)
            analysis_tab.columnconfigure(0, weight=1)
            analysis_tab.rowconfigure(0, weight=1)
            analysis_view.build(analysis_tab).pack(padx=10, pady=10, fill="both", expand=True)
            self._notebook.add(analysis_tab, text=analysis_view.get_name())
        return self._notebook

    def get_current_analysis_view(self) -> Optional[AnalysisView]:
        """
        gets the currently selected analysis view
        :return:    the currently selected analysis view
        """
        if len(self._analysis_views) == 0:
            showerror(
                EnglishTexts.ERROR_NO_ANALYSIS_VIEW_FOUND.value,
                EnglishTexts.INSTRUCTION_NO_ANALYSIS_VIEW_FOUND.value
            )
            return None
        index = self._notebook.index(self._notebook.select())
        return self._analysis_views[index]

    def add_analysis(self, data: AnalysisDataRecord, analysis_id: UUID):
        """
        adds a new analysis view tab
        :param analysis_id: the id of the analysis to add
        :param data: the analysis data to add
        """
        analysis_tab = ttk.Frame(self._notebook)
        analysis_tab.columnconfigure(0, weight=1)
        analysis_tab.rowconfigure(0, weight=1)
        analysis_view = self._analysis_view_factory.create_analysis_view(data, analysis_id)
        analysis_view.build(analysis_tab).pack(padx=10, pady=10, fill="both", expand=True)
        self._analysis_views.append(analysis_view)
        self._notebook.add(analysis_tab, text=data.data.name)

    def export_analysis(self, analysis_id: UUID, format: str) -> FileRecord:
        """
        exports the analysis view
        :param analysis_id: the id of the analysis id
        :param format:      the export format
        :return:            the file to export
        """
        pass

    def refresh_analysis(self, analysis_id: UUID, analyzed_data: AnalysisDataRecord):
        """
        refreshes the analysis view of the given id
        :param analysis_id:     the analysis id
        :param analyzed_data:   the analyzed data
        """
        for analysis in self._analysis_views:
            if analysis.id == analysis_id:
                analysis.refresh(analyzed_data)

    def delete_analysis(self, analysis_id: UUID):
        """
        deletes the analysis view of the given id
        :param analysis_id: the analysis id
        """
        for analysis in self._analysis_views:
            if analysis.id == analysis_id:
                index = self._analysis_views.index(analysis)
                self._analysis_views.remove(analysis)
                self._notebook.forget(index)
                return
