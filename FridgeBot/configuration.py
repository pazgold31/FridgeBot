import os

from FridgeBot.ArduinoCommunication.LimitSwitch import LimitSwitch
from FridgeBot.ArduinoCommunication.ArduinoCommunicator import ArduinoCommunicator
from FridgeBot.ArduinoCommunication.HumiditySensor import HumiditySensor
from FridgeBot.ArduinoCommunication.Motor import Motor
from FridgeBot.ArduinoCommunication.Relay import Relay
from FridgeBot.ArduinoCommunication.TemperatureSensor import TemperatureSensor
from FridgeBot.PiCode.Tasks.FridgeOpenFilter import FridgeOpenFilter, FridgeClosedFilter
from FridgeBot.PiCode.Tasks.FridgeTaskList import FridgeTaskList
from FridgeBot.PiCode.Tasks.FansActions import ActivateFansAction, DeactivateFansAction
from FridgeBot.PiCode.Tasks.RelayActions import ActivateRelayAction, DeactivateRelayAction
from FridgeBot.PiCode.Tasks.FridgeTask import FridgeTask
from FridgeBot.PiCode.Tasks.ScheduleFilter import ScheduleFilter
from FridgeBot.TaskList import TaskList

KEYS_FILE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "Bot", "keys.json")

Arduino = ArduinoCommunicator("/dev/ttyUSB0")

# Arduino = ArduinoCommunicator("COM5")

UV_LIGHT_RELAY = Relay(arduino=Arduino, pin=4, nc=True)
FAN_A = Motor(arduino=Arduino, direction_pin=12, break_pin=9, speed_pin=3)
FAN_B = Motor(arduino=Arduino, direction_pin=13, break_pin=8, speed_pin=11)
OPENING_SWITCH = LimitSwitch(arduino=Arduino, pin=2)
TEMPERATURE_SENSOR = TemperatureSensor(arduino=Arduino)
HUMIDITY_SENSOR = HumiditySensor(arduino=Arduino)

UV_ON_TIME = 20
UV_OFF_TIME = 30

FANS_ON_TIME = 20
FANS_OFF_TIME = 30

UV_LIGHT_TASKS = [
    FridgeTask(filters=[ScheduleFilter(time_offset=UV_OFF_TIME), FridgeClosedFilter(limit_switch=OPENING_SWITCH)],
               action=ActivateRelayAction(relay=UV_LIGHT_RELAY)),

    FridgeTask(filters=[ScheduleFilter(time_offset=UV_OFF_TIME + UV_ON_TIME)],
               action=DeactivateRelayAction(relay=UV_LIGHT_RELAY))
]

FANS_TASKS = [
    FridgeTask(filters=[ScheduleFilter(time_offset=FANS_OFF_TIME)],
               action=ActivateFansAction(fan1=FAN_A, fan2=FAN_B)),

    FridgeTask(filters=[ScheduleFilter(time_offset=FANS_OFF_TIME + FANS_ON_TIME)],
               action=DeactivateFansAction(fan1=FAN_A, fan2=FAN_B))
]

Tasks = TaskList([
    FridgeTaskList(tasks=UV_LIGHT_TASKS),  # Turn the UV on and off periodically.
    FridgeTaskList(tasks=FANS_TASKS),  # Turn the Fans on and off periodically.
    # FridgeTask(filters=[FridgeOpenFilter(limit_switch=OPENING_SWITCH)],  # Turn the uv off if the fridge is open
    #            action=DeactivateRelayAction(relay=UV_LIGHT_RELAY))
])
