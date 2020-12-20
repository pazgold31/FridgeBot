import logging

from FridgeBot.ArduinoCommunication.ArduinoCommunicator import ArduinoCommunicator


class Relay:
    def __init__(self, arduino: ArduinoCommunicator, pin:int, nc=True):
        self._arduino = arduino
        self._pin = pin
        self._nc = nc

    def on(self):
        # TODO: reverse according to NC
        logging.debug("Turning relay on on pin {}".format(self._pin))
        self._arduino.digital_set(self._pin, True)

    def off(self):
        # TODO: reverse according to NC
        logging.debug("Turning relay off on pin {}".format(self._pin))
        self._arduino.digital_set(self._pin, False)
