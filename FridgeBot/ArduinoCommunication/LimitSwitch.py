import logging

from FridgeBot.ArduinoCommunication.ArduinoCommunicator import ArduinoCommunicator


class LimitSwitch:
    def __init__(self, arduino: ArduinoCommunicator, pin: int, nc=True):
        self._arduino = arduino
        self._pin = pin
        self._nc = nc
        self._arduino.digital_set(pin=pin, status=True)

    def is_clicked(self) -> bool:
        logging.debug("Checking if Limit switch is clicked on pin {}".format(self._pin))
        res = self._arduino.digital_read(self._pin)
        logging.debug("Micro switch is: {}".format(res))
        return res
