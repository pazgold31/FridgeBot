import time

from FridgeBot.PiCode.Tasks.Tasks.IFridgeTask import IFridgeTask


class LinearFilterTask(IFridgeTask):
    def __init__(self, task: IFridgeTask, filter_time: int):
        self._task = task
        self._filter_time = filter_time
        self._next_available_run_timestamp = time.time() + self._filter_time

    def can_run(self) -> bool:
        if self._task.can_run():
            if time.time() >= self._next_available_run_timestamp:
                return True
        else:
            self._next_available_run_timestamp = time.time() + self._filter_time
            return False

    def is_finished(self) -> bool:
        return self._task.is_finished()

    def restart(self) -> None:
        self._task.restart()
        self._next_available_run_timestamp = time.time() + self._filter_time

    def run(self) -> None:
        try:
            self._task.run()
        finally:
            self._next_available_run_timestamp = time.time() + self._filter_time
