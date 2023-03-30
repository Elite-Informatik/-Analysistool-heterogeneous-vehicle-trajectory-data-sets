from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.view.user_interface.static_windows.main_window.main_window_elements.map_area.map import MapView

from tkintermapview.utility_functions import decimal_to_osm


class CanvasPoint:
    RADIUS = 3

    def __init__(self,
                 map_widget: "MapView",
                 position: list,
                 color: str = "red",
                 width: float = 1):
        """
        Constructor for a canvas point
        """

        self.map_widget = map_widget
        self.position = position
        self.canvas_point_position = ()
        self.deleted = False

        self.point_color = color
        self.canvas_point = None
        self.width = width
        self.highlight_width = width + 2

        self.last_upper_left_tile_pos = None
        self.last_position_list_length = len(self.position)

    def delete(self):
        """
        Deletes a canvas point
        """
        if self in self.map_widget.canvas_path_list:
            self.map_widget.canvas_points.remove(self)

        self.map_widget.canvas.delete(self.canvas_point)
        self.canvas_point = None
        self.deleted = True

    def get_canvas_pos(self, position, widget_tile_width, widget_tile_height):
        tile_position = decimal_to_osm(*position, round(self.map_widget.zoom))

        canvas_pos_x = ((tile_position[0] - self.map_widget.upper_left_tile_pos[
            0]) / widget_tile_width) * self.map_widget.width
        canvas_pos_y = ((tile_position[1] - self.map_widget.upper_left_tile_pos[
            1]) / widget_tile_height) * self.map_widget.height

        return canvas_pos_x, canvas_pos_y

    def draw(self, move=False):

        if move is True and self.last_upper_left_tile_pos is not None:
            self.canvas_point_position[0] += self.map_widget.x_move
            self.canvas_point_position[1] += self.map_widget.y_move

        else:
            self.canvas_point_position = []
            canvas_position = self.get_canvas_pos(self.position, self.map_widget.widget_tile_width,
                                                  self.map_widget.widget_tile_height)
            self.canvas_point_position.append(canvas_position[0])
            self.canvas_point_position.append(canvas_position[1])

        if not self.deleted:
            if self.canvas_point is None:
                self.map_widget.canvas.delete(self.canvas_point)
                self.canvas_point = self.map_widget.canvas.create_oval(self.canvas_point_position[0] + self.RADIUS,
                                                                       self.canvas_point_position[1] - self.RADIUS,
                                                                       self.canvas_point_position[0] - self.RADIUS,
                                                                       self.canvas_point_position[1] + self.RADIUS,
                                                                       fill=self.point_color,
                                                                       width=self.width,
                                                                       tags="point")

            else:
                self.map_widget.canvas.coords(self.canvas_point, self.canvas_point_position[0] + self.RADIUS,
                                              self.canvas_point_position[1] - self.RADIUS,
                                              self.canvas_point_position[0] - self.RADIUS,
                                              self.canvas_point_position[1] + self.RADIUS)

        else:
            self.map_widget.canvas.delete(self.canvas_point)
            self.canvas_point = None
