import logging

from FridgeBot.ArduinoCommunication.ArduinoCommunicator import ArduinoCommunicator


class Relay:
    def __init__(self, arduino: ArduinoCommunicator, pin: int, nc=True):
        self._arduino = arduino
        self._pin = pin
        self._nc = nc

    def on(self):
        logging.debug("Turning relay on on pin {}".format(self._pin))
        self._arduino.digital_set(self._pin, True ^ self._nc)

    def off(self):
        logging.debug("Turning relay off on pin {}".format(self._pin))
        self._arduino.digital_set(self._pin, False ^ self._nc)
