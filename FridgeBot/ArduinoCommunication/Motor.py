import logging

from FridgeBot.ArduinoCommunication.ArduinoCommunicator import ArduinoCommunicator


class Motor:
    def __init__(self, arduino: ArduinoCommunicator, direction_pin: int, break_pin: int, speed_pin: int,
                 inverted=False):
        self._arduino = arduino

        self._speed_pin = speed_pin
        self._break_pin = break_pin
        self._direction_pin = direction_pin

        self._inverted = inverted

    def forward(self, speed: int):
        logging.debug(
            "Driving motor forward on pins {} {} {}".format(self._direction_pin, self._break_pin, self._speed_pin))
        self._arduino.digital_set(self._direction_pin, not self._inverted)
        self._arduino.digital_set(self._break_pin, False)
        self._arduino.analog_set(self._speed_pin, speed)

    def backward(self, speed: int):
        logging.debug(
            "Driving motor backward on pins {} {} {}".format(self._direction_pin, self._break_pin, self._speed_pin))
        self._arduino.digital_set(self._direction_pin, self._inverted)
        self._arduino.digital_set(self._break_pin, False)
        self._arduino.analog_set(self._speed_pin, speed)

    def stop(self):
        logging.debug("stopping motor on pins {} {} {}".format(self._direction_pin, self._break_pin, self._speed_pin))
        self._arduino.digital_set(self._break_pin, True)
