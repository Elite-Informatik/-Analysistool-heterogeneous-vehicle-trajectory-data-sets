import tkinter as tk
from tkinter import DISABLED
from tkinter import END

from src.view.user_interface.dialogs.manual.manual_pages.manual_page import ManPage
from src.view.user_interface.ui_util.texts import EnglishTexts


class FilterManual(ManPage):
    """
    This manpage contains the manual for filters.
    """

    def build(self, master) -> tk.Frame:
        super().build(master)
        self._text_area.insert(END, introduction)
        self._text_area.insert(END, diff_heading, "heading")
        self._text_area.insert(END, diff_content)
        self._text_area.insert(END, create_heading, "heading")
        self._text_area.insert(END, create_steps)
        self._text_area.insert(END, delete_heading, "heading")
        self._text_area.insert(END, delete_steps)
        self._text_area.insert(END, edit_heading, "heading")
        self._text_area.insert(END, edit_steps)
        self._text_area.insert(END, add_heading, "heading")
        self._text_area.insert(END, add_steps)
        self._text_area.insert(END, group_heading, "heading")
        self._text_area.insert(END, group_content)
        self._text_area.insert(END, kind_heading, "heading")
        self._text_area.insert(END, kind_content)

        self._text_area.config(state=DISABLED)
        self._text_area.pack(fill="both", expand=True)
        return self._base_frame

    def get_title(self) -> str:
        return EnglishTexts.FILTER_MANUAL_TITLE.value


introduction: str = "In this section you can find a manual for filters.\n\n"
diff_heading: str = "Trajectory and datapoint filters\n"
diff_content: str = "Whats the difference between trajectory and datapoint filters?\n" \
                    "Trajectory filters are applied to the whole trajectory. " \
                    "A trajectory filter filters out all trajectories that do contain not one datapoint that fulfills the criteria. " \
                    "So after applying the filter, you can only see trajectories that contain at least one datapoint that fulfills the criteria.\n" \
                    "Datapoint filters are applied to each datapoint of a trajectory. " \
                    "A datapoint filter filters out all datapoint that does not fulfill the criteria.\n\n"

create_heading: str = "How to create a filter/ filter group:\n"
create_steps: str = "1. Right click on the datapoint or trajectory filter bar depending on what kind of filter/ filter group you want to create.\n" \
                    "2. Select the filter type and set the parameters. Press ok.\n" \
                    "3. The new filter/ filter group should now be displayed in the filter sidebar.\n" \
                    "4. The data will automatically be filtered. This can take some time. \n\n"

delete_heading: str = "How to delete a filter/ filter group:\n"
delete_steps: str = "1. Right click on filter/ filter group.\n" \
                    "2. Select delete and confirm the deletion.\n" \
                    "3. The filter/ filter group should now disappear from the filter bar " \
                    "and the data will automatically be filtered again.\n\n"

edit_heading: str = "How to edit a filter/ filter group:\n"
edit_steps: str = "1. Right click on the filte/ filter group.\n" \
                  "2. Select edit and change the parameters. Press ok.\n" \
                  "3. The data will automatically be filtered. This can take some time.\n\n"

add_heading: str = "How to add a filter/ filter group to a filter group:\n"
add_steps: str = "1. Right click on the filter group.\n" \
                 "2. Select add filter/ filter group and select the filter type and set the parameters. Press ok.\n" \
                 "3. The new filter/ filter group should now be displayed in the filter sidebar when unfolding the filter group.\n\n"

group_heading: str = "What is a filter group?\n"
group_content: str = "A filter group is a group that contains other filters. " \
                     "By selecting the logical operator AND or OR, you can choose how the contained filters are concatenated.\n\n"

kind_heading: str = "What are the different filter types?\n"
kind_content: str = "There are different filter types.\n" \
                    "An interval filter filters out all values that are not in the given interval. \n" \
                    "A discrete filter filters out all values that are not in the given discrete set of values. \n" \
                    "An area filter is a datapoint filter that filters out all datapoints that are not in the given area specified by the selected polygon. \n" \
                    "A transit filter is a trajectory filter that filters out all trajectories that do not run through the specified polygons.\n\n"
