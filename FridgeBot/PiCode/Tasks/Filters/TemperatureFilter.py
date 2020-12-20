from FridgeBot.ArduinoCommunication.TemperatureSensor import TemperatureSensor
from FridgeBot.PiCode.Tasks.Filters.IIFilter import IFilter


class TemperatureFilter(IFilter):
    def __init__(self, temperature_sensor: TemperatureSensor, max_temperature: float):
        self._temperature_sensor = temperature_sensor
        self._max_temperature = max_temperature

    def filter(self) -> bool:
        """
        Return true if the fridge is open
        """
        return self._max_temperature < self._temperature_sensor.get()

    def restart(self) -> None:
        pass
