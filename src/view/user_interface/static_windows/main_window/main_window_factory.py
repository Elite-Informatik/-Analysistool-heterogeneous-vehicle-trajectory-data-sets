import tkinter as tk

from src.data_transfer.content import FilterHandlerNames
from src.view.user_interface.static_windows.main_window.main_window_elements.map_area.map import MapView
from src.view.user_interface.static_windows.ui_element_factory import UiElementFactory


class MainWindowFactory(UiElementFactory):
    """
    A Factory that is used to create the MainWindow Elements and provides them with the required interfaces.
    Imports are done locally to prevent circular imports.
    """

    def create_main_window_base_frame(self):
        """
        Creates a new base frame of the main window
        """
        from src.view.user_interface.static_windows.main_window.main_window_elements.main_window_base_frame import \
            MainWindowBaseFrame
        return MainWindowBaseFrame(data_request=self._data_request,
                                   controller_communication=self._controller_communication,
                                   event_handler=self._event_handler,
                                   factory=self)

    def create_map_area(self):
        """
        Creates a new map area
        """
        from src.view.user_interface.static_windows.main_window.main_window_elements.map_area.map_area import MapArea
        return MapArea(data_request=self._data_request,
                       controller_communication=self._controller_communication,
                       event_handler=self._event_handler,
                       factory=self)

    def create_analysis_area(self):
        """
        Creates a new analysis area
        """
        from src.view.user_interface.static_windows.main_window.main_window_elements.analysis_area.analysis_area \
            import \
            AnalysisArea
        return AnalysisArea(data_request=self._data_request,
                            controller_communication=self._controller_communication,
                            event_handler=self._event_handler)

    def create_map(self, master: tk.Frame) -> MapView:
        """
        Creates a new map
        """
        return MapView(master=master, width=500, height=500)

    def create_polygon_sidebar(self):
        """
        Creates a new polygon sidebar
        """
        from src.view.user_interface.static_windows.main_window.main_window_elements.polygon_sidebar import \
            PolygonSideBar
        return PolygonSideBar(controller_communication=self._controller_communication,
                              data_request=self._data_request,
                              event_handler=self._event_handler)

    def create_menu_bar(self):
        """
        Creates a new menu bar
        """
        from src.view.user_interface.static_windows.main_window.main_window_elements.menu_bar import MenuBar
        return MenuBar(controller_communication=self._controller_communication,
                       data_request=self._data_request,
                       event_handler=self._event_handler)

    def create_trajectory_filter_bar(self):
        """
        Creates a new trajectory filter bar.
        The trajectory bar specific values are set here.
        """
        from src.view.user_interface.static_windows.main_window.main_window_elements.filter_sidebar import \
            FilterSidebar
        return FilterSidebar(controller_communication=self._controller_communication,
                             data_request=self._data_request,
                             event_handler=self._event_handler,
                             polygon_filter_name="Transit Filter",
                             filter_structure=FilterHandlerNames.TRAJECTORY_FILTER_HANDLER,
                             header_title="Trajectory Filters",
                             root_uuid=self._data_request.get_root_trajectory_filter())

    def create_datapoint_filter_bar(self):
        """
        Creates a new datapoint filter bar.
        The datapoint bar specific values are set here.
        """
        from src.view.user_interface.static_windows.main_window.main_window_elements.filter_sidebar import \
            FilterSidebar
        return FilterSidebar(controller_communication=self._controller_communication,
                             data_request=self._data_request,
                             event_handler=self._event_handler,
                             polygon_filter_name="Area Filter",
                             filter_structure=FilterHandlerNames.POINT_FILTER_HANDLER,
                             header_title="Datapoint Filters",
                             root_uuid=self._data_request.get_root_datapoint_filter())
