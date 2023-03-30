from ttkwidgets import CheckboxTreeview


class CheckBoxTreeView(CheckboxTreeview):
    """
    This class defines a checkbox tree view based on the CheckboxTreeview class.
    The purpose of this class is to define callback methods that are called when
    an item in the tree is checked or unchecked.
    """

    def __init__(self, check_callback: callable, uncheck_callback: callable, **kw):
        """
        Creates a new CheckBoxTreeView instance and sets the callback methods for
        checks and unchecks of an item.
        The callback methods must take a string as a parameter.
        The string defines the tree item that was checked or unchecked.
        """
        self._check_callback = check_callback
        self._uncheck_callback = uncheck_callback
        super().__init__(**kw)

    def _box_click(self, event):
        """
        Check or uncheck box when clicked.
        The right callback method is called.
        The callback methods are only called for the ancestors
        NOT for the descendants.
        """
        x, y, widget = event.x, event.y, event.widget
        elem = widget.identify("element", x, y)
        if "image" in elem:
            # a box was clicked
            item = self.identify_row(y)
            if self.tag_has("unchecked", item) or self.tag_has("tristate", item):
                self._check_callback(item)
            else:
                self._uncheck_callback(item)
