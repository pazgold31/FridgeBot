import time

from FridgeBot.PiCode.Tasks.IIFilter import IFilter


class ScheduleFilter(IFilter):
    def __init__(self, time_offset: int, restart_cooldown: int = 0):
        self._time_offset = time_offset
        self._restart_cooldown = restart_cooldown
        self._target_time = time.time() + time_offset

    def filter(self) -> bool:
        current_time = time.time()
        if current_time >= self._target_time:
            return True

        return False

    def restart(self) -> None:
        self._target_time = time.time() + self._time_offset + self._restart_cooldown
