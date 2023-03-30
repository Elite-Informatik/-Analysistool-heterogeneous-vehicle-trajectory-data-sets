import tkinter as tk

from src.view.controller_communication.controller_communication import ControllerCommunication
from src.view.data_request.data_request import DataRequest
from src.view.event_handler.i_event_hanlder_subscribe import IEventHandlerSubscribe
from src.view.user_interface.static_windows.main_window.main_window_factory import MainWindowFactory
from src.view.user_interface.static_windows.ui_element import UiElement


class MainWindowBaseFrame(UiElement):
    """
    The MainWindowBaseFrame is the Frame that contains the entire main window ui except the menu bar.
    It is responsible for defining the layout of the main window and performs the switch from the
    map to the analysis area.
    """

    def __init__(self,
                 controller_communication: ControllerCommunication,
                 data_request: DataRequest,
                 event_handler: IEventHandlerSubscribe,
                 factory: MainWindowFactory):
        super().__init__(controller_communication, data_request, event_handler)

        self._header = None
        self._button_to_map = None
        self._button_to_analysis = None
        self._body = None
        self._sidebar = None
        self._working_area = None
        # defines the current working area "map" or "analysis"
        self._current_working_area = ""
        self._factory = factory
        self._map_area = factory.create_map_area()
        self._analysis_area = factory.create_analysis_area()
        self._polygon_bar = factory.create_polygon_sidebar()
        self._trajectory_filter_bar = factory.create_trajectory_filter_bar()
        self._datapoint_filter_bar = factory.create_datapoint_filter_bar()

    def build(self, master: tk.Widget) -> tk.Widget:
        """
        See documentation of the UiElement class.
        """
        self._base_frame = tk.Frame(master=master, width=500, height=500)
        self._base_frame.columnconfigure(0, weight=1)
        self._base_frame.rowconfigure(0, weight=1)
        self._base_frame.rowconfigure(1, weight=25)
        self._base_frame.bind_all('<Control-z>', self.undo)
        self._base_frame.bind_all('<Control-y>', self.redo)

        # define header with buttons
        self._header = tk.Frame(master=self._base_frame)
        self._header.columnconfigure(0, weight=1)
        self._header.columnconfigure(1, weight=1)
        self._header.rowconfigure(0, weight=1)

        self._button_to_map = tk.Button(master=self._header, text="Map", command=self.switch_to_map, width=50)
        self._button_to_analysis = tk.Button(master=self._header, text="Analysis",
                                             command=self.switch_to_analysis, width=50)

        # define body with sidebar and working area
        self._body = tk.Frame(master=self._base_frame, width=200, height=100)
        self._body.columnconfigure(0, weight=1)
        self._body.columnconfigure(1, weight=7)
        self._body.rowconfigure(0, weight=1)

        self._sidebar = tk.Frame(master=self._body, width=50, height=200, padx=5)
        self._sidebar.columnconfigure(0, weight=1)
        self._sidebar.rowconfigure(0, weight=1)
        self._sidebar.rowconfigure(1, weight=1)

        trajectory_filter_bar = self._trajectory_filter_bar.build(self._sidebar)
        trajectory_filter_bar.grid(column=0, row=0, sticky="nsew")

        datapoint_filter_bar = self._datapoint_filter_bar.build(self._sidebar)
        datapoint_filter_bar.grid(column=0, row=1, sticky="nsew")

        polygon_bar = self._polygon_bar.build(self._sidebar)
        polygon_bar.grid(column=0, row=2, sticky="nsew")

        self._working_area = tk.Frame(master=self._body, width=250, height=200)
        self._working_area.columnconfigure(0, weight=1)
        self._working_area.rowconfigure(0, weight=1)

        self._header.grid(column=0, row=0, sticky="nsew")
        self._body.grid(column=0, row=1, sticky="nsew")

        self._button_to_map.grid(column=0, row=0, sticky="nsew")
        self._button_to_analysis.grid(column=1, row=0, sticky="nsew")

        self._sidebar.grid(column=0, row=0, sticky="nsew")
        self._working_area.grid(column=1, row=0, sticky="nsew")

        map = self._map_area.build(self._working_area)
        self._current_working_area = "map"
        map.grid(column=0, row=0, sticky="nsew")

        return self._base_frame

    def undo(self, event):
        """
        performs the undo action when the user presses the ctrl+z key combination.
        The method takes an event as input which is not used. It is necessary to have the event as input because
        the method is called by the bind_all method of tkinter and thus an event is passed to the method.
        """
        self._controller_communication.undo()

    def redo(self, event):
        """
        performs the redo action when the user presses the ctrl+y key combination.
        The method takes an event as input which is not used. It is necessary to have the event as input because
        the method is called by the bind_all method of tkinter and thus an event is passed to the method.
        """
        self._controller_communication.redo()


    def destroy(self):
        """
        See documentation of the UiElement class.
        """
        self._analysis_area.destroy()
        self._map_area.destroy()
        self._trajectory_filter_bar.destroy()
        self._datapoint_filter_bar.destroy()
        self._polygon_bar.destroy()
        self._base_frame.destroy()

    def switch_to_map(self):
        """
        performs the switch from the analysis area to the map area when the user clicks the Map button
        """
        if self._current_working_area != "map":
            self._current_working_area = "map"
            self._analysis_area.destroy()
            map = self._map_area.build(self._working_area)
            map.grid(column=0, row=0, sticky="nsew")

    def switch_to_analysis(self):
        """
        performs the switch from the map area to the analysis area when the user clicks the Analysis button
        """
        if self._current_working_area != "analysis":
            self._current_working_area = "analysis"
            self._map_area.destroy()
            analysis = self._analysis_area.build(self._working_area)
            analysis.grid(column=0, row=0, sticky="nsew")
