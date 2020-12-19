import logging

from FridgeBot.ArduinoCommunication.ArduinoCommunicator import ArduinoCommunicator


class HumiditySensor:
    def __init__(self, arduino: ArduinoCommunicator):
        self._arduino = arduino

    def get(self) -> float:
        logging.info("Checking humidity")
        return self._arduino.get_humidity()
