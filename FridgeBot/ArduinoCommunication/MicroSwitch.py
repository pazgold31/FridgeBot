import logging

from FridgeBot.ArduinoCommunication.ArduinoCommunicator import ArduinoCommunicator


class MicroSwitch:
    def __init__(self, arduino: ArduinoCommunicator, pin: int, nc=True):
        self._arduino = arduino
        self._pin = pin
        self._nc = nc

    def is_clicked(self) -> bool:
        logging.debug("Checking if microswitch is clicked on pin {}".format(self._pin))
        return self._arduino.digital_read(self._pin)
