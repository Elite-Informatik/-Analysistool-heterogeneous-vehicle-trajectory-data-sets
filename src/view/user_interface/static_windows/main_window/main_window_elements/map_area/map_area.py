import math
import tkinter as tk
from tkinter.messagebox import showerror
from tkinter.simpledialog import askstring
from typing import Dict
from typing import List
from typing import Tuple
from uuid import UUID

from PIL import ImageGrab
from PIL.Image import Image
from tkintermapview.canvas_path import CanvasPath
from tkintermapview.canvas_polygon import CanvasPolygon

from src.controller.output_handling.event import PolygonAdded
from src.controller.output_handling.event import PolygonChanged
from src.controller.output_handling.event import PolygonDeleted
from src.controller.output_handling.event import RefreshTrajectoryData
from src.controller.output_handling.event import SettingsChanged
from src.data_transfer.content.settings_enum import SettingsEnum
from src.data_transfer.record import TrajectoryRecord
from src.data_transfer.record.file_record_map import FileRecordMap
from src.view.controller_communication.controller_communication import ControllerCommunication
from src.view.data_request.data_request import DataRequest
from src.view.event_handler.event_consumers.polygon_event_consumer import PolygonEventConsumer
from src.view.event_handler.event_consumers.settings_event_consumer import SettingsEventConsumer
from src.view.event_handler.event_consumers.trajectory_event_consumer import TrajectoryEventConsumer
from src.view.event_handler.i_event_hanlder_subscribe import IEventHandlerSubscribe
from src.view.user_interface.dialogs.export_map import ExportMapDialog
from src.view.user_interface.static_windows.main_window.main_window_elements.map_area.canvas_point import CanvasPoint
from src.view.user_interface.static_windows.main_window.main_window_elements.map_area.map import MapView
from src.view.user_interface.static_windows.main_window.main_window_elements.map_area.map_button import MapButton
from src.view.user_interface.static_windows.main_window.main_window_elements.map_area.trajectory import Trajectory
from src.view.user_interface.static_windows.main_window.main_window_factory import MainWindowFactory
from src.view.user_interface.static_windows.ui_element import UiElement


def in_radius(point_a: Tuple, point_b: Tuple, radius: float) -> bool:
    """
    """
    distance = math.dist(point_a, point_b)
    if distance <= radius:
        return True
    return False


class MapArea(UiElement, SettingsEventConsumer, TrajectoryEventConsumer, PolygonEventConsumer):
    """
    """

    def __init__(self,
                 controller_communication: ControllerCommunication,
                 data_request: DataRequest,
                 event_handler: IEventHandlerSubscribe,
                 factory: MainWindowFactory):
        super().__init__(controller_communication, data_request, event_handler)

        self._create_polygon_button = None
        self._remove_polygon_button = None
        self._event_handler = event_handler
        event_handler.subscribe_polygon_events(self)
        event_handler.subscribe_settings_events(self)
        event_handler.subscribe_trajectory_events(self)

        self._zoom = None
        self._position = None

        self._factory = factory
        self._polygons_on_map: Dict[UUID, CanvasPolygon] = {}
        self._polygons: List[UUID] = []
        self._map: MapView = None
        self._map_trajectories: List[Trajectory] = []

        self._delete_polygon_mode: bool = False
        self._create_polygon_mode: bool = False

        self._POLYGON_POINT_IN_RANGE_RADIUS = lambda zoom: 3 / (1.82 ** zoom)
        self._polygon_in_creation: List[Tuple] = []
        self._polygon_in_creation_map_points: List[CanvasPoint] = []
        self._polygon_in_creation_map_segments: List[CanvasPath] = []

        # indicates if a map button has been clicked and thus the first coords passed are invalid
        # it is only used when the user presses on the create polygon button
        self._map_button_was_clicked = False

    def build(self, master: tk.Widget) -> tk.Widget:

        self._base_frame = tk.Frame(master=master, width=500, height=500)
        self._base_frame.rowconfigure(0, weight=1)
        self._base_frame.columnconfigure(0, weight=1)

        self._map: MapView = self._factory.create_map(master=self._base_frame)
        self._map.add_left_click_map_command(callback_function=self.left_click_map_command)
        self._map.add_right_click_menu_command(label="export map", command=self.export_map)
        self._map.grid(column=0, row=0, sticky="nsew")
        self._map.bind_all("<Button-3>", lambda event: self._reset_polygon_creation_process())
        # bind to button-2 to make it work on mac-os
        self._map.bind_all("<Button-2>", lambda event: self._reset_polygon_creation_process())

        self._create_polygon_button = MapButton(map_widget=self._map, canvas_position=(20, 100), text="+P",
                                                command=self.polygon_create_clicked)
        self._remove_polygon_button = MapButton(map_widget=self._map, canvas_position=(20, 140), text="-P",
                                                command=self.polygon_delete_clicked)

        # draw polygons
        for polygon in self._polygons:
            self.add_polygon_to_map(polygon_id=polygon)

        if self._zoom is None or self._position is None:
            self.calculate_and_set_map_position(trajectories=self._data_request.get_shown_trajectories())
        else:
            self._map.set_position(deg_x=self._position[0], deg_y=self._position[1])
            self._map.set_zoom(self._zoom)

        # draw trajectories
        self.reset_trajectories()
        return self._base_frame

    def calculate_and_set_map_position(self, trajectories: List[TrajectoryRecord]):
        latitudes = [latitude for trajectory in trajectories for latitude in trajectory.get_latitudes()]
        longitudes = [longitude for trajectory in trajectories for longitude in trajectory.get_longitudes()]
        if len(latitudes) == 0:
            average_latitude = 0
        else:
            average_latitude = sum(latitudes) / float(len(latitudes))
        if len(longitudes) == 0:
            average_longitude = 0
        else:
            average_longitude = sum(longitudes) / float(len(longitudes))
        self._map.set_position(deg_x=average_latitude, deg_y=average_longitude)
        self._map.set_zoom(zoom=10)

    def destroy(self):
        # clear polygons on map for the next map build
        if self._base_frame is None:
            return

        self._reset_polygon_creation_process()
        self._polygons_on_map.clear()
        self.delete_trajectories()
        self._zoom = self._map.zoom
        self._position = self._map.get_position()
        self._map_trajectories.clear()
        self._base_frame.destroy()
        self._base_frame = None
        self._map = None

    def left_click_map_command(self, coords):
        if self._create_polygon_mode:
            self.click_create_polygon(coords)

    def click_create_polygon(self, coords):
        # catches the first click on the create polygon button so the
        # start point of the polygon is not set on the button
        if self._map_button_was_clicked:
            self._map_button_was_clicked = False
            return
        if len(self._polygon_in_creation) == 0:
            self._polygon_in_creation.append(coords)
            self._polygon_in_creation_map_points.append(self._map.set_point(coords))
        elif len(self._polygon_in_creation) >= 3 and in_radius(coords,
                                                               self._polygon_in_creation[0],
                                                               radius=self._POLYGON_POINT_IN_RANGE_RADIUS(
                                                                   self._map.zoom)):
            self._polygon_in_creation_map_segments.append(
                self._map.set_path(position_list=[self._polygon_in_creation[0], self._polygon_in_creation[-1]],
                                   color="red",
                                   width=2))
            name = askstring(prompt="enter polygon name", title="Polygon Naming")
            if not name == "" and name is not None:
                self._controller_communication.add_polygon(position_list=self._polygon_in_creation, name=name)
            else:
                showerror(message="polygon can not be created")
            self._reset_polygon_creation_process()
        else:
            self._polygon_in_creation_map_points.append(self._map.set_point(coords))
            self._polygon_in_creation_map_segments \
                .append(self._map.set_path(position_list=[self._polygon_in_creation[-1], coords],
                                           color="red",
                                           width=2))
            self._polygon_in_creation.append(coords)

    def _reset_polygon_creation_process(self):
        for segment in self._polygon_in_creation_map_segments:
            segment.delete()
        for point in self._polygon_in_creation_map_points:
            point.delete()
        self._polygon_in_creation = []
        self._polygon_in_creation_map_points = []
        self._polygon_in_creation_map_segments = []
        self._create_polygon_mode = False
        self._create_polygon_button.set_disabled()

    def export_map(self):
        dialog = ExportMapDialog()
        if dialog.valid_input:
            img: Image = ImageGrab.grab((self._map.winfo_rootx(), self._map.winfo_rooty(),
                                         self._map.winfo_rootx() + self._map.winfo_width(),
                                         self._map.winfo_rooty() + self._map.winfo_height()))
            file = FileRecordMap(img, dialog.selected_file_name)
            self._controller_communication.export_file(file, dialog.selected_path)

    def add_polygon_to_map(self, polygon_id):
        polygon_data = self._data_request.get_polygon(polygon_id)
        positions_list = polygon_data.get_positions_as_list()
        polygon_on_map = self._map.set_polygon(position_list=positions_list, name=polygon_data.name,
                                               command=self.polygon_clicked, fill_color=None)
        self._polygons_on_map[polygon_id] = polygon_on_map

    def polygon_create_clicked(self):
        if self._create_polygon_mode:
            self.disable_polygon_creation()
        else:
            self.disable_polygon_deletion()
            self.enable_polygon_creation()

    def polygon_delete_clicked(self):
        if self._delete_polygon_mode:
            self.disable_polygon_deletion()
        else:
            self.disable_polygon_creation()
            self.enable_polygon_deletion()

    def enable_polygon_creation(self):
        self._map_button_was_clicked = True
        self._create_polygon_mode = True
        self._delete_polygon_mode = False
        self._create_polygon_button.set_enabled()

    def disable_polygon_creation(self):
        self._create_polygon_mode = False
        self._reset_polygon_creation_process()
        self._create_polygon_button.set_disabled()

    def enable_polygon_deletion(self):
        self._delete_polygon_mode = True
        self._reset_polygon_creation_process()
        self._create_polygon_mode = False
        self._remove_polygon_button.set_enabled()

    def disable_polygon_deletion(self):
        self._delete_polygon_mode = False
        self._remove_polygon_button.set_disabled()

    def polygon_clicked(self, polygon: CanvasPolygon):
        if self._delete_polygon_mode:
            for key, value in self._polygons_on_map.items():
                if value == polygon:
                    self._controller_communication.delete_polygon(uuid=key)

    def reset_trajectories(self):
        settings = self._data_request.get_settings()
        selections = settings.find(SettingsEnum.SHOW_LINE_SEGMENTS)
        selection = selections[0]
        show_line_segments = selection.selected[0]

        self.delete_trajectories()
        trajectories = self._data_request.get_shown_trajectories()
        for trajectory in trajectories:
            trajectory = self._map.set_trajectory(trajectory_data=trajectory,
                                                  get_trajectory_data=self._data_request.get_trajectory_data,
                                                  get_datapoint_data=self._data_request.get_datapoint_data,
                                                  show_line_segments=show_line_segments)
            self._map_trajectories.append(trajectory)

    def delete_trajectories(self):
        for trajectory in self._map_trajectories:
            trajectory.delete()
        self._map_trajectories = []

    def process_changed_settings(self, event: SettingsChanged):
        if self._map is not None:
            self.reset_trajectories()

    def process_added_polygon(self, event: PolygonAdded):
        self._polygons.append(event.id)
        if self._map is not None:
            self.add_polygon_to_map(event.id)

    def process_deleted_polygon(self, event: PolygonDeleted):
        self._polygons.remove(event.id)
        if self._map is not None:
            self._polygons_on_map[event.id].delete()

    def process_changed_polygon(self, event: PolygonChanged):
        if self._map is not None:
            self._polygons_on_map[event.id].delete()
            self.add_polygon_to_map(event.id)

    def process_refreshed_trajectory_data(self, event: RefreshTrajectoryData):
        if self._map is not None:
            self.reset_trajectories()
