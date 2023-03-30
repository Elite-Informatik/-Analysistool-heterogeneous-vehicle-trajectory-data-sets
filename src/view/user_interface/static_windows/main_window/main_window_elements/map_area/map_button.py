import math
import sys
import tkinter

from tkintermapview.canvas_button import CanvasButton


class MapButton(CanvasButton):
    """
    """

    def __init__(self, color_enabled: str = "grey", color_disabled: str = "black", *args, **kwargs):
        self._enabled_color = color_enabled
        self._disabled_color = color_disabled

        self._inner_color = self._disabled_color
        self._outer_color = self._disabled_color

        super().__init__(*args, **kwargs)

    def draw(self):
        """
        Copied from original implementation. Added colorization of button.
        """
        self.canvas_rect = self.map_widget.canvas.create_polygon(self.canvas_position[0], self.canvas_position[1],
                                                                 self.canvas_position[0] + self.width,
                                                                 self.canvas_position[1],
                                                                 self.canvas_position[0] + self.width,
                                                                 self.canvas_position[1] + self.height,
                                                                 self.canvas_position[0],
                                                                 self.canvas_position[1] + self.height,
                                                                 width=self.border_width,
                                                                 fill=self._disabled_color,
                                                                 outline=self._disabled_color,
                                                                 tag="button")

        self.canvas_text = self.map_widget.canvas.create_text(math.floor(self.canvas_position[0] + self.width / 2),
                                                              math.floor(self.canvas_position[1] + self.height / 2),
                                                              anchor=tkinter.CENTER,
                                                              text=self.text,
                                                              fill="white",
                                                              font="Tahoma 16",
                                                              tag="button")

        self.map_widget.canvas.tag_bind(self.canvas_rect, "<Button-1>", self.click)
        self.map_widget.canvas.tag_bind(self.canvas_text, "<Button-1>", self.click)
        self.map_widget.canvas.tag_bind(self.canvas_rect, "<Enter>", self.hover_on)
        self.map_widget.canvas.tag_bind(self.canvas_text, "<Enter>", self.hover_on)
        self.map_widget.canvas.tag_bind(self.canvas_rect, "<Leave>", self.hover_off)
        self.map_widget.canvas.tag_bind(self.canvas_text, "<Leave>", self.hover_off)

    def hover_on(self, event):

        if self.canvas_rect is not None:
            self.map_widget.canvas.itemconfig(self.canvas_rect, outline="grey")
            if sys.platform == "darwin":
                self.map_widget.canvas.config(cursor="pointinghand")
            elif sys.platform.startswith("win"):
                self.map_widget.canvas.config(cursor="hand2")
            else:
                self.map_widget.canvas.config(cursor="hand2")  # not tested what it looks like on Linux!

    def hover_off(self, event):

        self.map_widget.canvas.itemconfig(self.canvas_rect, outline=self._outer_color)
        self.map_widget.canvas.config(cursor="arrow")

    def set_disabled(self):

        self._inner_color = self._disabled_color
        self._outer_color = self._disabled_color
        self.set_colors(fill=self._inner_color, outline=self._outer_color)

    def set_enabled(self):

        self._inner_color = self._enabled_color
        self._outer_color = self._enabled_color
        self.set_colors(fill=self._inner_color, outline=self._outer_color)

    def set_colors(self, fill: str, outline: str):

        self.map_widget.canvas.itemconfig(self.canvas_rect, fill=fill, outline=outline)
