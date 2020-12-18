import serial
import struct

from enum import Enum

START_MAGIC = 0xabcd
SUCCESS_MESSAGE = b"\xab\xcd\x02"
ERROR_MESSAGE = b"\xab\xcd\x01"

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

    def send(self, data: bytes) -> None:
        self._arduino.write(data)

    def read(self, amount_of_bytes: int = 1) -> bytes:
        return self._arduino.read(amount_of_bytes)

    def digital_set(self, pin: int, status: bool) -> None:
        packet = struct.pack(">HBBBB", START_MAGIC, pin, PinMode.Digital.value, RequestType.Set.value,
                             1 if status else 0)
        self.send(data=packet)
        print(self.read(3))

    def close(self):
        self._arduino.close()
