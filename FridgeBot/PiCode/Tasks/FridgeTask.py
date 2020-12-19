from typing import List

from FridgeBot.PiCode.Tasks.IAction import IAction
from FridgeBot.PiCode.Tasks.IFridgeTask import IFridgeTask
from FridgeBot.PiCode.Tasks.IIFilter import IFilter


class FridgeTask(IFridgeTask):
    def __init__(self, filters: List[IFilter], action: IAction):
        self._filters = filters
        self._action = action
        self._is_finished = False

    def can_run(self) -> bool:
        for single_filter in self._filters:
            if not single_filter.filter():
                return False

        return True

    def restart(self) -> None:
        self._is_finished = False
        for single_filter in self._filters:
            single_filter.restart()
        self._action.restart()

    def is_finished(self) -> bool:
        return self._is_finished

    def run(self) -> None:
        self._action.run()
        self._is_finished = True
