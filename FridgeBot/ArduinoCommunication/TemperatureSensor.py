import logging

from FridgeBot.ArduinoCommunication.ArduinoCommunicator import ArduinoCommunicator


class TemperatureSensor:
    def __init__(self, arduino: ArduinoCommunicator):
        self._arduino = arduino

    def get(self) -> float:
        logging.debug("Checking Temperature")
        return self._arduino.get_temperature()
