from FridgeBot.ArduinoCommunication.Relay import Relay
from FridgeBot.PiCode.Tasks.IAction import IAction


class ActivateRelayAction(IAction):
    def __init__(self, relay: Relay):
        self._relay = relay

    def run(self) -> None:
        self._relay.on()

    def restart(self) -> None:
        pass


class DeactivateRelayAction(IAction):
    def __init__(self, relay: Relay):
        self._relay = relay

    def run(self) -> None:
        self._relay.off()

    def restart(self) -> None:
        pass
