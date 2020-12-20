from FridgeBot.ArduinoCommunication.LimitSwitch import LimitSwitch
from FridgeBot.PiCode.Tasks.Filters.IIFilter import IFilter


class FridgeOpenFilter(IFilter):
    def __init__(self, limit_switch: LimitSwitch):
        self._limit_switch = limit_switch

    def filter(self) -> bool:
        """
        Return true if the fridge is open
        """
        return not self._limit_switch.is_clicked()

    def restart(self) -> None:
        pass


class FridgeClosedFilter(IFilter):
    def __init__(self, limit_switch: LimitSwitch):
        self._limit_switch = limit_switch

    def filter(self) -> bool:
        """
        Return true if the fridge is closed
        """
        return self._limit_switch.is_clicked()

    def restart(self) -> None:
        pass
