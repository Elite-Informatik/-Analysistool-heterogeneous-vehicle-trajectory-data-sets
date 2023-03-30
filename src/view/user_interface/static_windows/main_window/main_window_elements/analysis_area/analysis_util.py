import re
from typing import List

import numpy as np
import pandas
from matplotlib import pyplot as plt, dates
from matplotlib.axes import Axes
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.text import Text
from pandas import DataFrame, Series
from pandas.api.types import is_string_dtype, is_numeric_dtype

from src.data_transfer.content import Column

MAX_ROTATE_LABELS = 3
MAX_LABELS = 15
MAX_NR_CHARS = 15
STRING_LABEL_ROTATION = 45
NON_NEGATIVE_DECIMALS_AND_INTS = "^[0-9]+(?:\.[0]*|)$"
DATETIME_PATTERN = "^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"
DATETIME_LABEL_PATTERN = "\d{2}-\d{2} \d{2}$"
TIME_REGEX = "\d{2}:\d{2}:\d{2}$"
TIME_FORMATTER = "%H:%M:%S"


def prepare_analysis_figure(master, x_name: str = "", y_name: str = "") -> FigureCanvasTkAgg:
    """
    creates a figure and sets the axis names
    :param master:      the master
    :param x_name:      the name of the x-axis
    :param y_name:      the name of the y-axis
    """
    figure = plt.Figure()
    figure.set_tight_layout(True)
    ax = figure.add_subplot(111)
    figure_canvas = FigureCanvasTkAgg(figure, master)
    # axis names
    ax.set_xlabel(x_name, fontsize=10)
    ax.set_ylabel(y_name, fontsize=10)
    return figure_canvas


# def prepare_columnformat(column: Series) -> Series:
#     if re.match(TIME_REGEX, str(column[0])):
#         return pandas.to_datetime(column, format=TIME_FORMATTER)
#     return column


def optimize_axes_labels(ax: Axes):
    """
    optimizes the axes labels:
    1) rotates string labels if there are too many, so they don't overlap
    2) converts labels of the time axis back to the time format
    :param ax:          the axes of the figure which labels are to optimize
    """
    _limit_label_length(ax)
    _optimize_nr_ticks(ax)
    _rotate_axes_labels(ax)

def _limit_label_length(ax: Axes):
    """
    limits the length of the labels to 10 characters
    :param ax:          the axes of the figure which labels are to optimize
    """
    if len(ax.get_xticklabels()[0].get_text()) > MAX_NR_CHARS:
        int_ticks = [str(x) for x in np.arange(1, len(ax.get_xticklabels()) + 1)]
        ax.set_xticklabels(int_ticks)
    if len(ax.get_yticklabels()[0].get_text()) > MAX_NR_CHARS:
        int_ticks = [str(x) for x in np.arange(1, len(ax.get_yticklabels()) + 1)]
        ax.set_yticklabels(int_ticks)

def _optimize_nr_ticks(ax: Axes):
    """
    optimizes the number of ticks on the axes
    :param ax:          the axes of the figure which labels are to optimize
    """
    # optimizes the number of ticks on the axes
    if len(ax.get_xticks()) > MAX_LABELS:
        ticks = ax.get_xticks()
        tick_labels = ax.get_xticklabels()
        step_size = len(ticks) // MAX_LABELS  # calculate the step size
        ticks = ticks[::step_size]  # create a list of ticks using the step size
        tick_labels = tick_labels[::step_size]  # create a list of tick labels using the step size
        ax.set_xticks(ticks)
        ax.set_xticklabels(tick_labels)
    labels = ax.get_yticklabels()
    labels = ax.get_yticks()
    if len(ax.get_yticks()) > MAX_LABELS:
        ticks = ax.get_yticks()
        tick_labels = ax.get_yticklabels()
        step_size = len(ticks) // MAX_LABELS  # calculate the step size
        ticks = ticks[::step_size]  # create a list of ticks using the step size
        tick_labels = tick_labels[::step_size]  # create a list of tick labels using the step size
        ax.set_yticks(ticks)
        ax.set_yticklabels(tick_labels)


# def _optimize_label_format(ax: Axes):
#     """
#     optimizes the formats of the columns in the dataframe:
#     1) converts datetime representations to datetime.time representation
#     :param ax:  the axes of the matplotlib diagram
#     """
#     first_x_label = ax.get_xticklabels()[0].get_text()
#     first_y_label = ax.get_yticklabels()[0].get_text()
#     if re.match(DATETIME_LABEL_PATTERN, first_x_label):
#         ax.xaxis.set_major_formatter(dates.DateFormatter(TIME_FORMATTER))
#     if re.match(DATETIME_LABEL_PATTERN, first_y_label):
#         ax.yaxis.set_major_formatter(dates.DateFormatter(TIME_FORMATTER))


def _rotate_axes_labels(ax: Axes):
    """
    rotates string labels if there are too many, so they don't overlap
    :param ax:          the axes of the figure which labels are to optimize
    """
    # rotates string labels if too many
    if len(ax.get_xticks()) > MAX_ROTATE_LABELS:
        ax.set_xticklabels(ax.get_xticklabels(), rotation=STRING_LABEL_ROTATION)


def _time_to_int(s: str) -> int:
    """
    converts a string in time format into an integer
    :param s:   the string in time format
    :return:    the integer
    """
    return int(''.join(s.split(':')))


def _int_to_time(i: int) -> str:
    """
    converts an integer back into time format
    :param i:   the integer in time format
    :return:    the string in time format
    """
    if i < 0:
        return ''
    time_str = '{}:{}:{}'.format(i // 10000, i % 10000 // 100, i % 100)
    return time_str


def time_column_to_int(time_column: List[str]) -> List[int]:
    """
    converts a column in time format into an integer column
    """
    return [_time_to_int(time) for time in time_column]


def int_column_to_time(int_column: List[int]) -> List[str]:
    """
    converts an integer column into a column in time format
    """
    return [_int_to_time(nr) for nr in int_column]
