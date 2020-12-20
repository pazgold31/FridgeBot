import time

from FridgeBot.PiCode.Tasks.Tasks.IFridgeTask import IFridgeTask


class CooldownTask(IFridgeTask):
    def __init__(self, task: IFridgeTask, cooldown: int):
        self._task = task
        self._cooldown = cooldown
        self._next_available_run_timestamp = time.time()

    def can_run(self) -> bool:
        return self._task.can_run() and time.time() >= self._next_available_run_timestamp

    def is_finished(self) -> bool:
        return self._task.is_finished()

    def restart(self) -> None:
        self._next_available_run_timestamp = time.time()
        self._task.restart()

    def run(self) -> None:
        try:
            self._task.run()
        finally:
            self._next_available_run_timestamp = time.time() + self._cooldown
