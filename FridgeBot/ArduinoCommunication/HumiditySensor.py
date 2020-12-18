import logging

from FridgeBot.ArduinoCommunication.ArduinoCommunicator import ArduinoCommunicator


class HumiditySensor:
    def __init__(self, arduino: ArduinoCommunicator, pin: int):
        self._arduino = arduino
        self._pin = pin

    def get(self) -> int:
        logging.debug("Checking humidity on pin {}".format(self._pin))
        return self._arduino.analog_read(self._pin)
