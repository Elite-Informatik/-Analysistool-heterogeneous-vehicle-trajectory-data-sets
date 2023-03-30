import math

from threading import Thread
from queue import Queue

from tkintermapview import TkinterMapView
from tkintermapview.canvas_polygon import CanvasPolygon
from tkintermapview.canvas_path import CanvasPath
from tkintermapview.canvas_position_marker import CanvasPositionMarker
from tkintermapview.canvas_tile import CanvasTile
from typing import List

from src.data_transfer.record import TrajectoryRecord
from src.view.user_interface.static_windows.main_window.main_window_elements.map_area.canvas_point import \
    CanvasPoint
from src.view.user_interface.static_windows.main_window.main_window_elements.map_area.trajectory import Trajectory


class MapView(TkinterMapView):
    """
    """
    def __init__(self, *args, **kwargs):
        self.canvas_points: List[CanvasPoint] = []
        self.trajectories: List[Trajectory] = []
        super().__init__(*args, **kwargs)
        self.last_upper_left_tile_pos = self.upper_left_tile_pos
        self.widget_tile_width = self.lower_right_tile_pos[0] - self.upper_left_tile_pos[0]
        self.widget_tile_height = self.lower_right_tile_pos[1] - self.upper_left_tile_pos[1]

        self._render_queue = Queue()
        self._render_thread = Thread(target=self._render_loop)
        self._render_thread.daemon = True
        self._render_thread.start()

    def _render_loop(self):
        while True:
            task = self._render_queue.get()
            try:
                task()
            except:
                pass
            self._render_queue.task_done()

    def clear_render_queue(self):
        self._render_queue.queue.clear()

    def wait_for_rendering(self):
        while not self._render_queue.empty():
            continue

    def set_point(self, position: List, **kwargs) -> CanvasPoint:
        point = CanvasPoint(map_widget=self, position=position, **kwargs)
        point.draw()
        self.canvas_points.append(point)
        return point

    def set_trajectory(self, trajectory_data: TrajectoryRecord, **kwargs) -> Trajectory:
        trajectory = Trajectory(map_widget=self, trajectory_data=trajectory_data, **kwargs)
        self.trajectories.append(trajectory)
        return trajectory

    def draw_move(self, called_after_zoom: bool = False):
        """
        copied the draw_move implementation from the TkinterMapView class and extend it to update the
        trajectories as well.
        """

        if self.canvas_tile_array:
            # insert or delete rows on top
            top_y_name_position = self.canvas_tile_array[0][0].tile_name_position[1]
            top_y_diff = self.upper_left_tile_pos[1] - top_y_name_position
            if top_y_diff <= 0:
                for y_diff in range(1, math.ceil(-top_y_diff) + 1):
                    self.insert_row(insert=0, y_name_position=top_y_name_position - y_diff)
            elif top_y_diff >= 1:
                for y_diff in range(1, math.ceil(top_y_diff)):
                    for x in range(len(self.canvas_tile_array) - 1, -1, -1):
                        if len(self.canvas_tile_array[x]) > 1:
                            self.canvas_tile_array[x][0].delete()
                            del self.canvas_tile_array[x][0]

            # insert or delete columns on left
            left_x_name_position = self.canvas_tile_array[0][0].tile_name_position[0]
            left_x_diff = self.upper_left_tile_pos[0] - left_x_name_position
            if left_x_diff <= 0:
                for x_diff in range(1, math.ceil(-left_x_diff) + 1):
                    self.insert_column(insert=0, x_name_position=left_x_name_position - x_diff)
            elif left_x_diff >= 1:
                for x_diff in range(1, math.ceil(left_x_diff)):
                    if len(self.canvas_tile_array) > 1:
                        for y in range(len(self.canvas_tile_array[0]) - 1, -1, -1):
                            self.canvas_tile_array[0][y].delete()
                            del self.canvas_tile_array[0][y]
                        del self.canvas_tile_array[0]

            # insert or delete rows on bottom
            bottom_y_name_position = self.canvas_tile_array[0][-1].tile_name_position[1]
            bottom_y_diff = self.lower_right_tile_pos[1] - bottom_y_name_position
            if bottom_y_diff >= 1:
                for y_diff in range(1, math.ceil(bottom_y_diff)):
                    self.insert_row(insert=len(self.canvas_tile_array[0]),
                                    y_name_position=bottom_y_name_position + y_diff)
            elif bottom_y_diff <= 1:
                for y_diff in range(1, math.ceil(-bottom_y_diff) + 1):
                    for x in range(len(self.canvas_tile_array) - 1, -1, -1):
                        if len(self.canvas_tile_array[x]) > 1:
                            self.canvas_tile_array[x][-1].delete()
                            del self.canvas_tile_array[x][-1]

            # insert or delete columns on right
            right_x_name_position = self.canvas_tile_array[-1][0].tile_name_position[0]
            right_x_diff = self.lower_right_tile_pos[0] - right_x_name_position
            if right_x_diff >= 1:
                for x_diff in range(1, math.ceil(right_x_diff)):
                    self.insert_column(insert=len(self.canvas_tile_array),
                                       x_name_position=right_x_name_position + x_diff)
            elif right_x_diff <= 1:
                for x_diff in range(1, math.ceil(-right_x_diff) + 1):
                    if len(self.canvas_tile_array) > 1:
                        for y in range(len(self.canvas_tile_array[-1]) - 1, -1, -1):
                            self.canvas_tile_array[-1][y].delete()
                            del self.canvas_tile_array[-1][y]
                        del self.canvas_tile_array[-1]

            # draw all canvas tiles
            for x_pos in range(len(self.canvas_tile_array)):
                for y_pos in range(len(self.canvas_tile_array[0])):
                    self.canvas_tile_array[x_pos][y_pos].draw()

            self.widget_tile_width = self.lower_right_tile_pos[0] - self.upper_left_tile_pos[0]
            self.widget_tile_height = self.lower_right_tile_pos[1] - self.upper_left_tile_pos[1]

            self.x_move = ((self.last_upper_left_tile_pos[0] - self.upper_left_tile_pos[0]) /
                      self.widget_tile_width) * self.width
            self.y_move = ((self.last_upper_left_tile_pos[1] - self.upper_left_tile_pos[1]) /
                      self.widget_tile_height) * self.height

            if not called_after_zoom:
                self.canvas.move("trajectory", self.x_move, self.y_move)
            else:
                self.canvas.delete("trajectory")
                self.clear_render_queue()
                for trajectory in self.trajectories:
                    self._render_queue.put(trajectory.redraw)


            # draw other objects on canvas
            for marker in self.canvas_marker_list:
                marker.draw()
            for path in self.canvas_path_list:
                path.draw(move=not called_after_zoom)
            for polygon in self.canvas_polygon_list:
                polygon.draw(move=not called_after_zoom)
            for point in self.canvas_points:
                point.draw(move=not called_after_zoom)


            self.manage_z_order()
            self.last_upper_left_tile_pos = self.upper_left_tile_pos

            # update pre-cache position
            self.pre_cache_position = (round((self.upper_left_tile_pos[0] + self.lower_right_tile_pos[0]) / 2),
                                       round((self.upper_left_tile_pos[1] + self.lower_right_tile_pos[1]) / 2))

    def draw_initial_array(self):
        self.image_load_queue_tasks = []

        x_tile_range = math.ceil(self.lower_right_tile_pos[0]) - math.floor(self.upper_left_tile_pos[0])
        y_tile_range = math.ceil(self.lower_right_tile_pos[1]) - math.floor(self.upper_left_tile_pos[1])

        # upper left tile _name position
        upper_left_x = math.floor(self.upper_left_tile_pos[0])
        upper_left_y = math.floor(self.upper_left_tile_pos[1])

        for x_pos in range(len(self.canvas_tile_array)):
            for y_pos in range(len(self.canvas_tile_array[0])):
                self.canvas_tile_array[x_pos][y_pos].__del__()

        # create tile array with size (x_tile_range x y_tile_range)
        self.canvas_tile_array = []

        for x_pos in range(x_tile_range):
            canvas_tile_column = []

            for y_pos in range(y_tile_range):
                tile_name_position = upper_left_x + x_pos, upper_left_y + y_pos

                image = self.get_tile_image_from_cache(round(self.zoom), *tile_name_position)
                if image is False:
                    # image is not in image cache, load blank tile and append position to image_load_queue
                    canvas_tile = CanvasTile(self, self.not_loaded_tile_image, tile_name_position)
                    self.image_load_queue_tasks.append(((round(self.zoom), *tile_name_position), canvas_tile))
                else:
                    # image is already in cache
                    canvas_tile = CanvasTile(self, image, tile_name_position)

                canvas_tile_column.append(canvas_tile)

            self.canvas_tile_array.append(canvas_tile_column)

        # draw all canvas tiles
        for x_pos in range(len(self.canvas_tile_array)):
            for y_pos in range(len(self.canvas_tile_array[0])):
                self.canvas_tile_array[x_pos][y_pos].draw()

        # draw other objects on canvas
        for marker in self.canvas_marker_list:
            marker.draw()
        for path in self.canvas_path_list:
            path.draw()
        for polygon in self.canvas_polygon_list:
            polygon.draw()
        for point in self.canvas_points:
            point.draw()

        # update pre-cache position
        self.pre_cache_position = (round((self.upper_left_tile_pos[0] + self.lower_right_tile_pos[0]) / 2),
                                   round((self.upper_left_tile_pos[1] + self.lower_right_tile_pos[1]) / 2))

    def delete(self, map_object: any):
        if isinstance(map_object, (CanvasPath, CanvasPositionMarker, CanvasPolygon, CanvasPoint, Trajectory)):
            map_object.delete()

    def manage_z_order(self):
        """
        Defines the layering of the different map elements.
        """
        self.canvas.lift("polygon")
        self.canvas.lift("path")
        self.canvas.lift("marker")
        self.canvas.lift("marker_image")
        self.canvas.lift("corner")
        self.canvas.lift("trajectory")
        self.canvas.lift("point")
        self.canvas.lift("button")
