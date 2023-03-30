import tkinter as tk
from tkinter import ttk
from typing import Dict
from typing import List
from uuid import UUID

from tktooltip import ToolTip

from src.controller.output_handling.event import FilterAdded
from src.controller.output_handling.event import FilterChanged
from src.controller.output_handling.event import FilterComponentDeleted
from src.controller.output_handling.event import FilterGroupAdded
from src.controller.output_handling.event import FilterGroupChanged
from src.controller.output_handling.event import FilterMovedToGroup
from src.data_transfer.content.global_constants import FilterHandlerNames
from src.data_transfer.record import FilterGroupRecord
from src.data_transfer.record import FilterRecord
from src.view.controller_communication.controller_communication import ControllerCommunication
from src.view.data_request.data_request import DataRequest
from src.view.event_handler.event_consumers.filter_event_consumer import FilterEventConsumer
from src.view.event_handler.i_event_hanlder_subscribe import IEventHandlerSubscribe
from src.view.user_interface.dialogs import CreateDiscreteFilterDialog
from src.view.user_interface.dialogs import CreateFilterGroupDialog
from src.view.user_interface.dialogs import CreateIntervalFilterDialog
from src.view.user_interface.dialogs import CreatePolygonFilterDialog
from src.view.user_interface.dialogs.filter_creator import FilterCreator
from src.view.user_interface.static_windows.main_window.main_window_elements.check_box_tree_view import CheckBoxTreeView
from src.view.user_interface.static_windows.ui_element import UiElement
from src.view.user_interface.ui_util.texts import EnglishTexts


class FilterSidebar(UiElement, FilterEventConsumer):
    """
    The FilterSidebar is a class that represents a Filter bar. It defines all methods a filter bar needs.
    Some attributes that make up the small difference between the datapoint filter-bar and the
    trajectory filter-bar are defined in the concrete Subclasses.
    A Filter Sidebar is a FilterEventConsumer. It reacts on Filter Events and can refresh its View
    based on the events.
    """

    # selectable filter types
    POLYGON_FILTER = "polygon filter"
    DISCRETE_FILTER = "discrete filter"
    INTERVAL_FILTER = "interval filter"

    def __init__(self, controller_communication: ControllerCommunication,
                 data_request: DataRequest,
                 event_handler: IEventHandlerSubscribe,
                 header_title: str,
                 filter_structure: FilterHandlerNames,
                 polygon_filter_name: str,
                 root_uuid: UUID):
        super().__init__(controller_communication, data_request, event_handler)

        self._event_handler.subscribe_filter_events(self)

        self._add_filter_menu = None
        self._standard_menu = None
        self._filter_group_menu = None
        self._filter_menu = None

        self._header_title = header_title
        self._filter_structure: FilterHandlerNames = filter_structure
        self._polygon_filter_name: str = polygon_filter_name
        self._root_uuid: UUID = root_uuid

        # maps the filters to the element id in the TreeView structure
        self._uuid_to_tree_id: Dict[UUID, str] = {self._root_uuid: ""}
        self._tree_id_to_uuid: Dict[str, UUID] = {"": self._root_uuid}
        self._filter_tree: ttk.Treeview = None

        # caches the clicked tree item so other methods can determine which item was clicked when they handle a click
        # default value is "" determines that no item was clicked
        self._clicked_tree_item: str = ""

        self._concrete_filters: List[UUID] = []
        self._filter_groups: List[UUID] = []

    def build(self, master: tk.Widget) -> tk.Widget:
        """
        See UiElement.build for documentation
        """
        # setup baseframe
        self._base_frame = tk.Frame(master=master)
        self._base_frame.rowconfigure(0, weight=1)
        self._base_frame.columnconfigure(0, weight=1)

        # initialize tree view
        # todo add filters to the structure at initialisation
        self._filter_tree = CheckBoxTreeView(master=self._base_frame,
                                             check_callback=self.enable_filter,
                                             uncheck_callback=self.disable_filter)
        self._filter_tree.heading("#0", text=self._header_title)
        self._filter_tree.bind("<Button-3>", self.right_click)
        self._filter_tree.bind("<Button-2>", self.right_click)
        self._filter_tree.grid(column=0, row=0, sticky="nsew")

        # define context menu that is opened when the tree is clicked without hitting a tree element.
        self._standard_menu = tk.Menu(master=self._filter_tree, tearoff=0)
        add_filter_menu = self._build_add_filter_context_menu(master=self._standard_menu)
        self._standard_menu.add_cascade(label="+add Filter", menu=add_filter_menu)
        self._standard_menu.add_command(label="+add Filter Group", command=self.create_filter_group)

        # define context menu that is opened when the user clicks on a filter group
        self._filter_group_menu = tk.Menu(master=self._filter_tree, tearoff=0)
        add_filter_menu = self._build_add_filter_context_menu(master=self._filter_group_menu)
        self._filter_group_menu.add_cascade(label="+add Filter", menu=add_filter_menu)
        self._filter_group_menu.add_command(label="+add Filter Group", command=self.create_filter_group)
        self._filter_group_menu.add_command(label="edit Filter Group", command=self.edit_filter_group)
        self._filter_group_menu.add_command(label="delete Filter", command=self.delete_filter)

        # define context menu that is opened when the user clicks on a concrete filter
        self._filter_menu = tk.Menu(master=self._filter_tree, tearoff=0)
        self._filter_menu.add_command(label="edit Filter", command=self.edit_concrete_filter)
        self._filter_menu.add_command(label="delete Filter", command=self.delete_filter)

        ToolTip(self._filter_tree, msg=EnglishTexts.SIDEBAR_TIP.value, delay=0.5)

        return self._base_frame

    def _build_add_filter_context_menu(self, master: tk.Menu) -> tk.Menu:
        """
        Builds the context menu that is opened when the user wants to create a new filter.
        The build of this menu is extern because it is used in two different context menus.
        """
        # define context menu that is opened when the user wants to create a new filter.
        add_filter_menu = tk.Menu(master=master, tearoff=0)
        add_filter_menu.add_command(label=self.INTERVAL_FILTER,
                                    command=lambda: self.create_concrete_filter(self.INTERVAL_FILTER))
        add_filter_menu.add_command(label=self.DISCRETE_FILTER,
                                    command=lambda: self.create_concrete_filter(self.DISCRETE_FILTER))
        add_filter_menu.add_command(label=self._polygon_filter_name,
                                    command=lambda: self.create_concrete_filter(self.POLYGON_FILTER))
        return add_filter_menu

    def destroy(self):
        """
        Sets the filter_tree to None so other methods can see if the sidebar is currently build.
        """
        self._uuid_to_tree_id = {self._root_uuid: ""}
        self._tree_id_to_uuid = {"": self._root_uuid}
        if self._base_frame is not None:
            self._base_frame.destroy()
        self._filter_tree = None
        self._base_frame = None

    def right_click(self, event=None):
        """
        Defines how to handle a right click on the tree view structure.
        The context menu based on the click location is opened and the clicked item will be cached.
        The clicked item can than be used to determine which item was clicked,
        when the context menu executes a function.
        """
        if event is None:
            pass
        item = self._filter_tree.identify("item", event.x, event.y)
        self._clicked_tree_item = item
        if item == "":
            self._standard_menu.tk_popup(event.x_root, event.y_root)
        else:
            uuid = self._tree_id_to_uuid[item]
            if uuid in self._filter_groups:
                self._filter_group_menu.tk_popup(event.x_root, event.y_root)
            if uuid in self._concrete_filters:
                self._filter_menu.tk_popup(event.x_root, event.y_root)

    def _from_filter_group_dialog_to_controller(self, dialog: CreateFilterGroupDialog, edit: bool = False) -> bool:
        """
        Takes a dialog and reads the filter group form the dialog. If the dialog is valid the filter group will be
        sent to the controller. Based on the new_filter_group parameter the filter group will be sent as a new
        filter group or as an old filter group that has been modified
        :param dialog: the dialog that contains the filter data
        :param edit: decides if the filter group will be passed via add_filter_group(False) or
        change_filter_group(True)
        :return: True if the dialogs was valid otherwise False
        """
        if dialog.is_valid():
            group = dialog.get_new_filter_group()
            # meaning of the group id depends on if the filter group was created(parent)
            # or edited(id for the edited group)
            group_id = self._tree_id_to_uuid[self._clicked_tree_item]
            if not edit:
                self._controller_communication.add_filter_group(filter_group_record=group, parent=group_id)
            else:
                self._controller_communication.change_filter_group(group_id=group_id, group_data=group)
            return True
        return False

    def create_filter_group(self):
        """
        Method that spans the dialog for the filter group creation.
        """
        standard_filter_group = self._data_request.get_standard_filter_group()
        dialog = CreateFilterGroupDialog(filter_group_record=standard_filter_group,
                                         structure_name=self._filter_structure.value)
        self._from_filter_group_dialog_to_controller(dialog=dialog)
        self._clicked_tree_item = None

    def edit_filter_group(self):
        """
        Method that spawns the dialog for the filter group editing.
        """
        filter_group_id = self._tree_id_to_uuid[self._clicked_tree_item]
        filter_group_data = self._data_request.get_filter_group(filter_group=filter_group_id)
        dialog = CreateFilterGroupDialog(filter_group_record=filter_group_data,
                                         structure_name=self._filter_structure.value,
                                         edit=True)
        self._from_filter_group_dialog_to_controller(dialog=dialog, edit=True)
        self._clicked_tree_item = None

    def _from_filter_dialog_to_controller(self, dialog: FilterCreator, edit: bool = False) -> bool:
        """
        Takes a dialog and reads the concrete filter from the dialog. If the dialog is valid the filter will be
        sent to the controller. Based on the new_filter parameter the filter will be sent as a new filter or as
        an old filter that has been modified.
        :param dialog: the dialog that contains the filter data
        :param edit: decides if the filter will be passed via add_filter(False) or change_filter(True)
        :return: True if the dialog was valid otherwise False
        """
        if dialog.is_valid():
            filter = dialog.get_new_filter()
            # meaning of the group id depends on if the filter group was created(parent)
            # or edited(id for the edited group)
            changed_filter_or_parent = self._tree_id_to_uuid[self._clicked_tree_item]
            if not edit:
                self._controller_communication.add_filter(filter=filter, parent=changed_filter_or_parent)
            else:
                self._controller_communication.change_filter(filter_id=changed_filter_or_parent, filter_data=filter)
            return True
        return False

    def create_concrete_filter(self, filter_type: str):
        """
        Method that spawns the dialog for the creation of a new filter
        :params filter_type: the type of filter that the user wants to create
        """
        standard_filter = self._data_request.get_standard_filter(filter_type=filter_type)
        if standard_filter.type == "discrete filter":
            dialog = CreateDiscreteFilterDialog(filter_record=standard_filter,
                                                structure_name=self._filter_structure.value,
                                                selection_callback=self._data_request.get_discrete_selection_column)
        if standard_filter.type == "interval filter":
            dialog = CreateIntervalFilterDialog(filter_record=standard_filter,
                                                structure_name=self._filter_structure.value,
                                                selection_callback=self._data_request.get_interval_selection_column)
        if standard_filter.type == "polygon filter":
            dialog = CreatePolygonFilterDialog(filter_record=standard_filter,
                                               structure_name=self._filter_structure.value)
        self._from_filter_dialog_to_controller(dialog=dialog)
        self._clicked_tree_item = None

    def edit_concrete_filter(self):
        """
        Method that spawns the dialog for the filter editing.
        """
        filter_id = self._tree_id_to_uuid[self._clicked_tree_item]
        filter_record = self._data_request.get_filter(filter_id)
        if filter_record.type == "interval filter":
            dialog = CreateIntervalFilterDialog(filter_record=filter_record,
                                                structure_name=self._filter_structure.value,
                                                selection_callback=self._data_request.get_interval_selection_column,
                                                edit=True)
        if filter_record.type == "discrete filter":
            dialog = CreateDiscreteFilterDialog(filter_record=filter_record,
                                                structure_name=self._filter_structure.value,
                                                selection_callback=self._data_request.get_interval_selection_column,
                                                edit=True)
        if filter_record.type == "polygon filter":
            dialog = CreatePolygonFilterDialog(filter_record=filter_record,
                                               structure_name=self._filter_structure.value,
                                               edit=True)
        self._from_filter_dialog_to_controller(dialog, edit=True)
        self._clicked_tree_item = None

    def delete_filter(self):
        """
        Method that deletes the clicked filter component
        """
        # _clicked_tree_item can not be "" because the delete feature can only be executed when
        # a tree component hat been clicked
        deleted_component_id = self._tree_id_to_uuid[self._clicked_tree_item]
        self._controller_communication.delete_filter(filter_component_id=deleted_component_id)
        self._clicked_tree_item = None

    def enable_filter(self, item: str):
        """
        callback method that is put to the CheckboxTree and called by the CheckboxTree when
        an item is checked.
        :param item: the tree item that was checked.
        """
        uuid = self._tree_id_to_uuid[item]
        if uuid in self._filter_groups:
            filter_group = self._data_request.get_filter_group(filter_group=uuid)
            self._controller_communication.change_filter_group(group_id=uuid, group_data=filter_group.enable())

        else:
            filter_data = self._data_request.get_filter(filter_id=uuid)
            self._controller_communication.change_filter(filter_id=uuid, filter_data=filter_data.enable())

    def disable_filter(self, item: str):
        """
        callback method that is put to the CheckboxTree and called by the CheckboxTree when
        an item is unchecked.
        :param item: the tree item that was unchecked.
        """
        uuid = self._tree_id_to_uuid[item]
        if uuid in self._filter_groups:
            filter_group = self._data_request.get_filter_group(filter_group=uuid)
            self._controller_communication.change_filter_group(group_id=uuid, group_data=filter_group.disable())

        else:
            filter_data = self._data_request.get_filter(filter_id=uuid)
            self._controller_communication.change_filter(filter_id=uuid, filter_data=filter_data.disable())

    def _filter_group_to_tree(self, filter_group_data: FilterGroupRecord, tree_parent: str) -> str:
        """
        Method that creates a tree item for a filter group and puts it into the tree
        :param filter_group_data: the filter group data that is used to create the tree item
        :param tree_parent: the parent of the tree item
        :return: the id of the created tree item
        """
        if filter_group_data.enabled:
            tag = "checked"
        else:
            tag = "unchecked"
        return self._filter_tree.insert(tree_parent, "end", text=filter_group_data.__repr__(), tags=tag)

    def _change_group_entry(self, filter_group_data: FilterGroupRecord, tree_id: str):
        """
        Method that changes the text and state of a filter group tree element
        :param filter_group_data: the new filter group data
        :param tree_id: the id of the tree element to which the filter group belongs
        """
        self._filter_tree.item(tree_id, text=filter_group_data.__repr__())
        if filter_group_data.enabled:
            self._filter_tree.change_state(tree_id, "checked")
        else:
            self._filter_tree.change_state(tree_id, "unchecked")

    def _filter_to_tree(self, filter_data: FilterRecord, tree_parent: str) -> str:
        """
        Method that creates a tree item for a filter and puts it into the tree.
        :param filter_data: the filter data that is used to create the tree item
        :param tree_parent: the parent of the tree item
        :return: the id of the created tree item
        """
        text = f"{filter_data.name} - {filter_data.type}"
        if filter_data.enabled:
            tag = "checked"
        else:
            tag = "unchecked"
        return self._filter_tree.insert(tree_parent, "end", text=text, tags=tag)

    def _change_filter_entry(self, filter_data: FilterRecord, tree_id: str):
        """
        Method that changes the text and state of a filter tree element
        :param filter_data: the new filter data
        :param tree_id: the id of the tree element to which the filter belongs
        """
        text = f"{filter_data.name} - {filter_data.type}"
        self._filter_tree.item(tree_id, text=text)
        if filter_data.enabled:
            self._filter_tree.change_state(tree_id, "checked")
        else:
            self._filter_tree.change_state(tree_id, "unchecked")

    # ------ event processing -------
    def process_deleted_filter(self, event: FilterComponentDeleted):
        """
        This method processes the delete filter event. It is necessary to proof if the filter actually belongs to
        this filter structure. The filter data can not be requested from the data request interface because it
        has already been deleted in the model.
        :param event: the event containing the uuid of the filter that has been deleted.
        """
        belongs_to_this_structure = False

        if event.id in self._filter_groups:
            self._filter_groups.remove(event.id)
            belongs_to_this_structure = True
        if event.id in self._concrete_filters:
            belongs_to_this_structure = True
            self._concrete_filters.remove(event.id)

        if not belongs_to_this_structure:
            return
        tree_id = self._uuid_to_tree_id[event.id]
        # if a filter group is deleted the child elements in the tree are deleted as well.
        # In the case that for each child an own delete event is sent, the child elements do not need
        # to be deleted from the tree. But the mappings for uuids and tree ids still need to be cleaned up.
        if self._filter_tree.exists(item=tree_id):
            self._filter_tree.delete(tree_id)

        del self._uuid_to_tree_id[event.id]
        del self._tree_id_to_uuid[tree_id]

    def process_added_filter(self, event: FilterAdded):
        """
        This Method processes the added filter event. It is necessary to proof if the new filter actually belongs
        to this filter structure.
        :param event: the event containing the id of the new filter and the id of the filter group to which the
        filter belongs
        """
        filter_data = self._data_request.get_filter(event.id)
        if not filter_data.structure_name == self._filter_structure.value:
            return

        self._concrete_filters.append(event.id)
        if self._base_frame is not None:
            parent_tree_element = self._uuid_to_tree_id[event.group_id]
            tree_id = self._filter_to_tree(filter_data=filter_data, tree_parent=parent_tree_element)
            self._uuid_to_tree_id[event.id] = tree_id
            self._tree_id_to_uuid[tree_id] = event.id

    def process_changed_filter(self, event: FilterChanged):
        """
        This method processes the changed filter event. It is necessary to proof if the changed filter actually belongs
        to this filter structure.
        :param event: the event containing the id of the changed filter.
        """
        filter_data = self._data_request.get_filter(event.id)
        if not filter_data.structure_name == self._filter_structure.value:
            return

        if self._base_frame is not None:
            tree_id = self._uuid_to_tree_id[event.id]
            self._change_filter_entry(filter_data=filter_data, tree_id=tree_id)

    def process_added_filter_group(self, event: FilterGroupAdded):
        """
        This method processes the added filter group event. It is necessary to proof if the new filter group actually
        belongs to this filter structure.
        :param event: the event containing the id of the new filter group and the group id to which the new
        filter group belongs
        """
        filter_group_data = self._data_request.get_filter_group(event.id)
        if not filter_group_data.structure_name == self._filter_structure.value:
            return

        self._filter_groups.append(event.id)
        if self._base_frame is not None:
            parent_tree_element = self._uuid_to_tree_id[event.group_id]
            tree_id = self._filter_group_to_tree(filter_group_data=filter_group_data, tree_parent=parent_tree_element)
            self._uuid_to_tree_id[event.id] = tree_id
            self._tree_id_to_uuid[tree_id] = event.id

    def process_changed_filter_group(self, event: FilterGroupChanged):
        """
        This method processes the changed filter group event. It is necessary to proof if the changed filter group
        actually belongs to this filter structure.
        :param event: the event containing the id of the changed filter group
        """
        filter_group_data = self._data_request.get_filter_group(event.id)
        if not filter_group_data.structure_name == self._filter_structure.value:
            return

        if self._base_frame is not None:
            tree_id = self._uuid_to_tree_id[event.id]
            self._change_group_entry(filter_group_data=filter_group_data, tree_id=tree_id)

    def process_moved_filter(self, event: FilterMovedToGroup):
        """
        Moving Filters is currently not supported. The method still needed to be declared to fulfill the requirements
        of the filter event consumer interface.
        """
        raise NotImplementedError("Moving Filters in the Tree View is not implemented yet")
