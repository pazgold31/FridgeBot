import logging
import time
from threading import Lock

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
    GetTemperature = 3
    GetHumidity = 4


class ArduinoCommunicator:
    def __init__(self, serial_port: str):
        self._arduino = serial.Serial(serial_port, baudrate=9600, timeout=5)
        self._arduino.flushInput()
        self._arduino.flushOutput()
        time.sleep(2)  # Giving arduino some time to initialize.
        self._lock = Lock()

    def _validate_request_successful(self) -> None:
        received_message = self._read(len(SUCCESS_MESSAGE))
        if SUCCESS_MESSAGE != received_message:
            if received_message[:len(ERROR_MESSAGE)] == ERROR_MESSAGE:
                error_code = received_message[-1]
                logging.error("Received an error from arduino, error code: {code}".format(code=error_code))
            else:
                logging.error("Arduino returned an invalid message")

            raise RuntimeError

    def _get_read_result(self) -> int:
        self._validate_request_successful()
        returned_value = self._read()
        return ord(returned_value)

    def _send(self, data: bytes) -> None:
        self._arduino.write(data)

    def send(self, data: bytes) -> None:
        with self._lock:
            self._send(data=data)

    def _read(self, amount_of_bytes: int = 1) -> bytes:
        return self._arduino.read(amount_of_bytes)

    def read(self, amount_of_bytes: int = 1) -> bytes:
        with self._lock:
            return self._read(amount_of_bytes=amount_of_bytes)

    def digital_set(self, pin: int, status: bool) -> None:
        with self._lock:
            packet = struct.pack(">HBBBB", START_MAGIC, pin, PinMode.Digital.value, RequestType.Set.value,
                                 1 if status else 0)
            self._send(data=packet)
            self._validate_request_successful()

    def digital_read(self, pin: int) -> bool:
        with self._lock:
            packet = struct.pack(">HBBBB", START_MAGIC, pin, PinMode.Digital.value, RequestType.Read.value, 0)
            self._send(data=packet)
            return True if self._get_read_result() else False

    def analog_set(self, pin: int, status: int) -> None:
        with self._lock:
            packet = struct.pack(">HBBBB", START_MAGIC, pin, PinMode.Analog.value, RequestType.Set.value, status)
            self._send(data=packet)
            self._validate_request_successful()

    def analog_read(self, pin: int) -> int:
        with self._lock:
            packet = struct.pack(">HBBBB", START_MAGIC, pin, PinMode.Analog.value, RequestType.Read.value, 0)
            self._send(data=packet)
            return self._get_read_result()

    def get_temperature(self) -> float:
        with self._lock:
            packet = struct.pack(">HBBBB", START_MAGIC, 0, 0, RequestType.GetTemperature.value, 0)
            self._send(data=packet)
            self._validate_request_successful()
            arg = self._read(4)
            return struct.unpack("f", arg)[0]

    def get_humidity(self) -> float:
        with self._lock:
            packet = struct.pack(">HBBBB", START_MAGIC, 0, 0, RequestType.GetHumidity.value, 0)
            self._send(data=packet)
            self._validate_request_successful()
            arg = self._read(4)
            return struct.unpack("f", arg)[0]

    def close(self):
        with self._lock:
            self._arduino.close()
