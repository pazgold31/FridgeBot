import logging

import serial
import struct

from enum import Enum

START_MAGIC = 0xabcd
SUCCESS_MESSAGE = b"\xab\xcd\x01"
ERROR_MESSAGE = b"\xab\xcd"


class PinMode(Enum):
    Digital = 1
    Analog = 2


class RequestType(Enum):
    Set = 1
    Read = 2


class ArduinoCommunicator:
    def __init__(self, serial_port: str):
        self._arduino = serial.Serial(serial_port, baudrate=9600, timeout=5)
        self._arduino.flushInput()
        self._arduino.flushOutput()

    def _validate_request_successful(self) -> None:
        received_message = self.read(len(SUCCESS_MESSAGE))
        if SUCCESS_MESSAGE != received_message:
            if received_message[:len(ERROR_MESSAGE)] == ERROR_MESSAGE:
                error_code = received_message[-1]
                logging.error("Received an error from arduino, error code: {code}", code=error_code)
            else:
                logging.error("Arduino returned an invalid message")

            raise RuntimeError

    def _get_read_result(self) -> int:
        self._validate_request_successful()
        returned_value = self.read()
        return ord(returned_value)

    def send(self, data: bytes) -> None:

        self._arduino.write(data)

    def read(self, amount_of_bytes: int = 1) -> bytes:
        return self._arduino.read(amount_of_bytes)

    def digital_set(self, pin: int, status: bool) -> None:
        packet = struct.pack(">HBBBB", START_MAGIC, pin, PinMode.Digital.value, RequestType.Set.value,
                             1 if status else 0)
        self.send(data=packet)
        self._validate_request_successful()

    def digital_read(self, pin: int) -> bool:
        packet = struct.pack(">HBBBB", START_MAGIC, pin, PinMode.Digital.value, RequestType.Read.value)
        self.send(data=packet)
        return True if self._get_read_result() else False

    def analog_set(self, pin: int, status: int) -> None:
        packet = struct.pack(">HBBBB", START_MAGIC, pin, PinMode.Analog.value, RequestType.Set.value, status)
        self.send(data=packet)
        self._validate_request_successful()

    def analog_read(self, pin: int) -> int:
        packet = struct.pack(">HBBBB", START_MAGIC, pin, PinMode.Analog.value, RequestType.Read.value)
        self.send(data=packet)
        return self._get_read_result()

    def close(self):
        self._arduino.close()
