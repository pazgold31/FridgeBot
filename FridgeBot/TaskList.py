import copy
from typing import List

from FridgeBot.PiCode.Tasks.FridgeTask import FridgeTask


class TaskList(list):
    def __init__(self, lst: List[FridgeTask]):
        self._original_list = copy.copy(lst)
        super(TaskList, self).__init__(lst)

    def __getitem__(self, key):
        return self[key]

    def __setitem__(self, key, item):
        self[key] = item

    def execute(self, item) -> None:
        if item in self._original_list:
            item.restart()
        else:
            self.pop(self.index(item))
