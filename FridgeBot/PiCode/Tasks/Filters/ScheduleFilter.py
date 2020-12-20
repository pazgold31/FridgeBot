import time

from FridgeBot.PiCode.Tasks.Filters.IIFilter import IFilter


class ScheduleFilter(IFilter):
    def __init__(self, time_offset: int):
        self._time_offset = time_offset
        self._target_time = time.time() + time_offset

    def filter(self) -> bool:
        current_time = time.time()
        if current_time >= self._target_time:
            return True

        return False

    def restart(self) -> None:
        self._target_time = time.time() + self._time_offset
