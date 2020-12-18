from FridgeBot.PiCode.Tasks.IAction import IAction
from FridgeBot.PiCode.Tasks.IIFilter import IFilter


class FridgeTask:
    def __init__(self, filter: IFilter, action: IAction):
        self._filter = filter
        self._action = action

    def can_run(self) -> bool:
        return self._filter.filter()

    def restart(self) -> None:
        self._filter.restart()
        self._action.restart()

    def run(self) -> None:
        self._action.run()
