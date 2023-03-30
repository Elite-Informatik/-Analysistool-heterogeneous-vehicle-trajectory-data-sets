from tkinter import ttk
from tkinter.ttk import Notebook
import tkinter as tk

from src.view.user_interface.dialogs.manual.manual_pages.analysis_manual import AnalysisManual
from src.view.user_interface.dialogs.manual.manual_pages.dataformat_manual import DataformatManual
from src.view.user_interface.dialogs.manual.manual_pages.filter_manual import FilterManual
from src.view.user_interface.dialogs.manual.manual_pages.map_manual import MapManual
from src.view.user_interface.dialogs.manual.manual_pages.polygon_manual import PolygonManual
from src.view.user_interface.dialogs.manual.manual_pages.dataset_manual import DatasetManual


class ManualNotebook:
    """
    This class is responsible to manage the manual pages
    """

    def __init__(self):
        self._notebook: Notebook = None
        self._man_pages = [AnalysisManual, MapManual, FilterManual, PolygonManual, DatasetManual, DataformatManual]

    def build(self, master) -> tk.Widget:
        """
        builds the ManualNotebook
        :param master:  the master
        :return:        the widget containing the manual notebook
        """
        self._notebook = ttk.Notebook(master=master, height=500, width=500)
        self._notebook.columnconfigure(0, weight=1)
        self._notebook.rowconfigure(0, weight=1)
        for man_page in self._man_pages:
            page_tab = ttk.Frame(self._notebook)
            page_tab.columnconfigure(0, weight=1)
            page_tab.rowconfigure(0, weight=1)
            man_page().build(page_tab).pack(padx=10, pady=10, fill="both", expand=True)
            self._notebook.add(page_tab, text=man_page().get_title())
        return self._notebook
