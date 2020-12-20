from FridgeBot.ArduinoCommunication.Motor import Motor
from FridgeBot.PiCode.Tasks.Actions.IAction import IAction


class ActivateFansAction(IAction):
    def __init__(self, fan1: Motor, fan2: Motor):
        self._fan2 = fan2
        self._fan1 = fan1

    def run(self) -> None:
        self._fan1.forward(255)
        self._fan2.forward(255)

    def restart(self) -> None:
        pass


class DeactivateFansAction(IAction):
    def __init__(self, fan1: Motor, fan2: Motor):
        self._fan2 = fan2
        self._fan1 = fan1

    def run(self) -> None:
        self._fan1.stop()
        self._fan2.stop()

    def restart(self) -> None:
        pass
