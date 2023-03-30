import tkinter as tk
from tkinter import DISABLED
from tkinter import END

from src.view.user_interface.dialogs.manual.manual_pages.manual_page import ManPage
from src.view.user_interface.ui_util.texts import EnglishTexts


class AnalysisManual(ManPage):
    """
    This manpage contains the manual for analyses
    """

    def build(self, master) -> tk.Frame:
        super().build(master)
        self._text_area.insert(END, introduction)
        self._text_area.insert(END, creation_heading, "heading")
        self._text_area.insert(END, creation_steps)
        self._text_area.insert(END, kind_description)
        self._text_area.insert(END, plot_heading, "heading")
        self._text_area.insert(END, plot_description)
        self._text_area.insert(END, path_time_heading, "heading")
        self._text_area.insert(END, path_time_description)
        self._text_area.insert(END, path_daytime_heading, "heading")
        self._text_area.insert(END, path_daytime_description)
        self._text_area.insert(END, src_dest_heading, "heading")
        self._text_area.insert(END, src_dest_description)
        self._text_area.insert(END, transmission_heading, "heading")
        self._text_area.insert(END, transmission_description)
        self._text_area.insert(END, table_heading, "heading")
        self._text_area.insert(END, table_description)
        self._text_area.insert(END, total_param_heading, "heading")
        self._text_area.insert(END, total_param_description)
        self._text_area.insert(END, average_param_heading, "heading")
        self._text_area.insert(END, average_param_description)
        self._text_area.insert(END, histogram_heading, "heading")
        self._text_area.insert(END, histogram_description)
        self._text_area.insert(END, heatmap_heading, "heading")
        self._text_area.insert(END, heatmap_description)

        self._text_area.config(state=DISABLED)
        self._text_area.pack(fill="both", expand=True)
        return self._base_frame

    def get_title(self) -> str:
        return EnglishTexts.ANALYSIS_MANUAL_TITLE.value


introduction: str = "In this section you can find a manual for the different analyses.\n\n"
creation_heading: str = "How to create a new analysis:\n"
creation_steps: str = "1. Click on the 'Create' button. \n" \
                      "2. Select the analysis kind and press ok. \n" \
                      "3. The new analysis should now be displayed in a new tab. To change the default parameters, click on the 'Change' button.\n\n"

kind_description: str = "In the following you can find an explanation for all available analysis kinds: \n\n"

plot_heading: str = "Plot\n"
plot_description: str = "This analysis kind allows you to plot two parameters against each other.\n\n"

path_time_heading: str = "Path Time Analysis\n"
path_time_description: str = "This analysis plots time against the distance taken.\n\n"

path_daytime_heading: str = "Path Daytime Analysis\n"
path_daytime_description: str = "This analysis plots time against the distance taken. " \
                                "Here the time is not relative to the start of the analysis but instead the absolute daytime.\n\n"

src_dest_heading: str = "Source Destination Analysis\n"
src_dest_description: str = "It calculates the time taken from the start polygon to the end polygon, the distance, as well as the average speed. " \
                            "It does this for each trajectory individually and also calculates the mean.\n\n"

transmission_heading: str = "Transmission Analysis\n"
transmission_description: str = "This analysis kind analyzes the transmission frequency of a given dataset. " \
                                "When choosing the parameter 'average', the average time difference for each trajectory is displayed. " \
                                "When choosing the parameter 'distribution', the distribution of the time difference between two datapoints is displayed in a histogram.\n\n"

table_heading: str = "Table Analysis\n"
table_description: str = "This analysis kind displays the selected columns in a table.\n\n"

total_param_heading: str = "Total Parameter Analysis\n"
total_param_description: str = "This analysis kind calculates the number of unique values in non-numeric columns.\n\n"

average_param_heading: str = "Average Parameter Analysis\n"
average_param_description: str = "This analysis kind calculates the average of numeric columns and mode of non-numeric columns.\n\n"

histogram_heading: str = "Histogram Analysis\n"
histogram_description: str = "This analysis kind creates a histogram for the selected column.\n\n"

heatmap_heading: str = "Heatmap Analysis\n"
heatmap_description: str = "This analysis kind creates a heatmap for the three selected columns.\n\n"
