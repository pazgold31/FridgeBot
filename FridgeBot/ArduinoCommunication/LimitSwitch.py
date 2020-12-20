import logging

from FridgeBot.ArduinoCommunication.ArduinoCommunicator import ArduinoCommunicator


class LimitSwitch:
    def __init__(self, arduino: ArduinoCommunicator, pin: int, nc=True):
        self._arduino = arduino
        self._pin = pin
        self._nc = nc

    def is_clicked(self) -> bool:
        logging.debug("Checking if Limit switch is clicked on pin {}".format(self._pin))
        self._arduino.digital_set(pin=self._pin, status=True)
        return self._arduino.digital_read(self._pin) == self._nc
