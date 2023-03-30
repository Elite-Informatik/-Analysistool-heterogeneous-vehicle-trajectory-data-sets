import tkinter as tk
from typing import List
from typing import TYPE_CHECKING
from uuid import UUID

import pandas as pd
from pandastable import Table
from tkintermapview.utility_functions import decimal_to_osm

from src.data_transfer.record import DataPointRecord
from src.data_transfer.record import DataRecord
from src.data_transfer.record import TrajectoryRecord

if TYPE_CHECKING:
    from src.view.user_interface.static_windows.main_window.main_window_elements.map_area.map import MapView

GREYED_OUT_COLOR = "grey"


class Trajectory:
    """
    Defines a Trajectory that is drawn on the map. The trajectory holds all data that is needed for
    the trajectory to be displayed on the map.
    """

    RADIUS = 3
    POINT_WIDTH = 1
    SEGMENT_WIDTH = 3
    POINT_HIGHLIGHT_WIDTH = 3
    SEGMENT_HIGHLIGHT_WIDTH = 5

    def __init__(self, map_widget: "MapView", trajectory_data: TrajectoryRecord,
                 get_trajectory_data: callable, get_datapoint_data: callable,
                 show_line_segments: bool):
        """
        Creates a new Trajectory based on a Trajectory Record.
        :params map_widget: the map widget on which the trajectories should be drawn
        :param trajectory_data: The Trajectory data
        :param get_datapoint_data: a method that takes an uuid of a datapoint and returns the raw data of the datapoint
        :param get_trajectory_data: a method tha takes an uuid of a trajectory and
        returns the raw data of the trajectory
        """
        self.map_widget = map_widget
        self.trajectory_data = trajectory_data
        self._show_line_segments = show_line_segments

        self._points: List = []
        self._segments: List = []
        self._get_datapoint_data = get_datapoint_data
        self._get_trajectory_data = get_trajectory_data

        self._trajectory_record = trajectory_data

        self._uuid = trajectory_data.id
        # caches the datapoint that was clicked
        self._clicked_datapoint: UUID = None

        self._trajectory_click_menu = tk.Menu(master=map_widget.canvas, tearoff=0)
        self._trajectory_click_menu.add_command(label="show trajectory data", command=self.show_trajectory_data)

        self._datapoint_click_menu = tk.Menu(master=map_widget.canvas, tearoff=0)
        self._datapoint_click_menu.add_command(label="show datapoint data", command=self.show_datapoint_data)
        self._datapoint_click_menu.add_command(label="show trajectory data", command=self.show_trajectory_data)

        self.redraw()

    def redraw(self):
        """
        This method clears all canvas elements that belong to the trajectory and then
        recreates all canvas elements that belong to the trajectory and puts them on the map.
        This method should only be used for the zoom redraw and not for basic move operations since
        this method is quite inefficient compared to moving all elements by the same x and y diffs.
        For zooming this method is still used, because each element is moved by different x and y diffs in the canvas.
        """
        self.clear()
        datapoints = self.trajectory_data.datapoints
        for i in range(len(datapoints) - 1):
            # in each iteration the i-th point and the i-th line segment is drawn
            start_point: DataPointRecord = datapoints[i]
            end_point: DataPointRecord = datapoints[i + 1]

            start_position = start_point.get_position_as_tuple()
            end_position = end_point.get_position_as_tuple()

            start_canvas_pos = self.get_canvas_pos(start_position, self.map_widget.widget_tile_width,
                                                   self.map_widget.widget_tile_height)
            end_canvas_pos = self.get_canvas_pos(end_position, self.map_widget.widget_tile_width,
                                                 self.map_widget.widget_tile_height)

            start_point_color = self.convert_int_to_hex_color(start_point.visualisation)
            line_segment_color = self.convert_int_to_hex_color(
                round((start_point.visualisation + end_point.visualisation) / 2))

            canvas_point = self.map_widget.canvas.create_oval(start_canvas_pos[0] + self.RADIUS,
                                                              start_canvas_pos[1] - self.RADIUS,
                                                              start_canvas_pos[0] - self.RADIUS,
                                                              start_canvas_pos[1] + self.RADIUS,
                                                              fill=start_point_color,
                                                              width=self.POINT_WIDTH,
                                                              tags=["trajectory", "point"])
            self.map_widget.canvas.tag_bind(canvas_point, "<Button-1>",
                                            lambda event: self.datapoint_clicked(event, start_point.id))
            self._points.append(canvas_point)
            canvas_line = self.map_widget.canvas.create_line(start_canvas_pos[0], start_canvas_pos[1],
                                                             end_canvas_pos[0], end_canvas_pos[1],
                                                             fill=line_segment_color,
                                                             width=self.SEGMENT_WIDTH,
                                                             tags=["trajectory", "segment"])
            self.map_widget.canvas.tag_bind(canvas_line, "<Button-1>", self.trajectory_clicked)
            self._segments.append(canvas_line)

        if len(datapoints) > 0:
            last_point = datapoints[-1]
            last_point_position = last_point.get_position_as_tuple()
            canvas_position = self.get_canvas_pos(last_point_position, self.map_widget.widget_tile_width,
                                                  self.map_widget.widget_tile_height)
            color = self.convert_int_to_hex_color(last_point.visualisation)
            canvas_point = self.map_widget.canvas.create_oval(canvas_position[0] + self.RADIUS,
                                                              canvas_position[1] - self.RADIUS,
                                                              canvas_position[0] - self.RADIUS,
                                                              canvas_position[1] + self.RADIUS,
                                                              fill=color,
                                                              width=self.POINT_WIDTH,
                                                              tags=["trajectory", "point"])
            self.map_widget.canvas.tag_bind(canvas_point, "<Button-1>",
                                            lambda event: self.datapoint_clicked(event, start_point.id))
            self._points.append(canvas_point)

        if self._show_line_segments is False:
            self.turn_off_line_segments()

        for point in self._points:
            self.map_widget.canvas.tag_bind(point, "<Enter>", lambda event: self.highlight_trajectory())
            self.map_widget.canvas.tag_bind(point, "<Leave>", lambda event: self.lowlight_trajectory())
        for segment in self._segments:
            self.map_widget.canvas.tag_bind(segment, "<Enter>", lambda event: self.highlight_trajectory())
            self.map_widget.canvas.tag_bind(segment, "<Leave>", lambda event: self.lowlight_trajectory())
        self.map_widget.canvas.lift("point")

    def get_canvas_pos(self, position, widget_tile_width, widget_tile_height):
        """
        Returns the canvas position for a given coordinate tuple
        """
        tile_position = decimal_to_osm(*position, round(self.map_widget.zoom))

        canvas_pos_x = ((tile_position[0] - self.map_widget.upper_left_tile_pos[
            0]) / widget_tile_width) * self.map_widget.width
        canvas_pos_y = ((tile_position[1] - self.map_widget.upper_left_tile_pos[
            1]) / widget_tile_height) * self.map_widget.height

        return canvas_pos_x, canvas_pos_y

    def turn_off_line_segments(self):
        """
        Hides the line segments of the trajectories
        """
        for segment in self._segments:
            self.map_widget.canvas.itemconfigure(segment, state=tk.HIDDEN)
        self._show_line_segments = False

    def turn_on_line_segments(self):
        """
        Shows the line segments of the trajectories again
        """
        for segment in self._segments:
            self.map_widget.canvas.itemconfigure(segment, state=tk.NORMAL)
        self._show_line_segments = True

    def trajectory_clicked(self, event):
        """
        opens the trajectory context menu when the menu was clicked
        """
        self._trajectory_click_menu.tk_popup(event.x_root, event.y_root)

    def show_trajectory_data(self):
        """
        gets the data for the trajectory with the uuid of this instance and displays it in a new window
        """
        trajectory_data_record: DataRecord = self._get_trajectory_data(trajectory_id=self._uuid)
        data = trajectory_data_record.data
        self._display_raw_data(data=data, title="Trajectory Data")

    def datapoint_clicked(self, event, datapoint_id: UUID):
        """
        opens the context enum of a datapoint
        """
        self._clicked_datapoint = datapoint_id
        self._datapoint_click_menu.tk_popup(event.x_root, event.y_root)

    def show_datapoint_data(self):
        """
        gets the data for the clicked datapoint and displays it in a new window
        """
        datapoint_data_record: DataRecord = self._get_datapoint_data(datapoint_id=self._clicked_datapoint)
        data = datapoint_data_record.data
        self._display_raw_data(data=data, title="Datapoint Data")
        self._clicked_datapoint = None

    def _display_raw_data(self, data: pd.DataFrame, title: str):
        """
        Creates a new Window and displays a dataframe in the window.
        :param data: the dataframe that should be displayed
        :param title: the title of the window
        """
        window = tk.Toplevel()
        window.title(title)
        window.grab_set()
        table = Table(window, dataframe=data, editable=False)
        table.show()

    def highlight_trajectory(self):
        """
        highlights the trajectory on the map
        """
        for segment in self._segments:
            self.map_widget.canvas.itemconfigure(segment, width=self.SEGMENT_HIGHLIGHT_WIDTH)
        for point in self._points:
            self.map_widget.canvas.itemconfigure(point, width=self.POINT_HIGHLIGHT_WIDTH)

    def lowlight_trajectory(self):
        """
        disables the highlighting on the map
        """
        for segment in self._segments:
            self.map_widget.canvas.itemconfigure(segment, width=self.SEGMENT_WIDTH)
        for point in self._points:
            self.map_widget.canvas.itemconfigure(point, width=self.POINT_WIDTH)

    def delete(self):
        """
        Deletes the trajectory from the map and removes the trajectory from the trajectory list of the map widget.
        Afterwards all references to the trajectory except the reference of the caller should be deleted.
        Furthermore al canvas elements of the trajectory are deleted.
        """
        if self in self.map_widget.trajectories:
            self.map_widget.trajectories.remove(self)
        self.clear()

    def clear(self):
        """
        Deletes all canvas elements of the trajectory
        """
        for point in self._points:
            self.map_widget.canvas.delete(point)
        for segment in self._segments:
            self.map_widget.canvas.delete(segment)
        self._points = []
        self._segments = []

    @staticmethod
    def convert_int_to_hex_color(rgb_int) -> str:
        """
        Converts an integer to a hex color string with the format #RRGGBB
        """
        r = (rgb_int >> 16) & 0xFF
        g = (rgb_int >> 8) & 0xFF
        b = rgb_int & 0xFF
        hex_code = "#{0:02x}{1:02x}{2:02x}".format(r, g, b)
        return hex_code
