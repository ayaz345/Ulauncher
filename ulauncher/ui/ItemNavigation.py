from ulauncher.config import PATHS
from ulauncher.utils.json_data import JsonData

query_history = JsonData.new_from_file(f"{PATHS.STATE}/query_history.json")


class ItemNavigation:
    """
    Performs navigation through found results
    """

    index = 0

    def __init__(self, result_widgets):
        """
        :param list result_widgets: list of ResultWidget()'s
        """
        self.result_widgets = result_widgets

    @property
    def selected_item(self):
        if self.index is not None and len(self.result_widgets) > self.index:
            return self.result_widgets[self.index]
        return None

    def get_default(self, query):
        """
        Gets the index of the result that should be selected (0 by default)
        """
        previous_pick = query_history.get(query)

        return next(
            (
                index
                for index, widget in enumerate(self.result_widgets)
                if widget.result.searchable and widget.result.name == previous_pick
            ),
            0,
        )

    def select_default(self, query):
        self.select(self.get_default(query))

    def select(self, index):
        if not 0 < index < len(self.result_widgets):
            index = 0

        if self.selected_item:
            self.selected_item.deselect()

        self.index = index
        self.result_widgets[index].select()

    def go_up(self):
        self.select((self.index or len(self.result_widgets)) - 1)

    def go_down(self):
        next_result = (self.index or 0) + 1
        self.select(next_result if next_result < len(self.result_widgets) else 0)

    def activate(self, query, alt=False):
        """
        Return boolean - True if Ulauncher window should be kept open
        """
        result = self.selected_item.result
        if query and not alt and result.searchable:
            query_history.save({str(query): result.name})

        return result.on_activation(query, alt)
