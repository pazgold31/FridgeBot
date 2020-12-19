from typing import List
from FridgeBot.PiCode.Tasks.IFridgeTask import IFridgeTask


class FridgeTaskList(IFridgeTask):
    def __init__(self, tasks: List[IFridgeTask]):
        if 0 == len(tasks):
            raise RuntimeError("List must contains at least one task!")
        self._tasks = tasks
        self._current_task_index = 0

    def can_run(self) -> bool:
        return self._tasks[self._current_task_index].can_run()

    def is_finished(self) -> bool:
        for task in self._tasks:
            if not task.is_finished():
                return False

        return True

    def restart(self) -> None:
        for task in self._tasks:
            task.restart()

    def run(self) -> None:
        self._tasks[self._current_task_index].run()
        self._current_task_index = (self._current_task_index + 1) % len(self._tasks)
