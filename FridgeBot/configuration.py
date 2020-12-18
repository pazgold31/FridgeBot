from FridgeBot.ArduinoCommunication.ArduinoCommunicator import ArduinoCommunicator
from FridgeBot.ArduinoCommunication.HumiditySensor import HumiditySensor
from FridgeBot.ArduinoCommunication.Motor import Motor
from FridgeBot.ArduinoCommunication.Relay import Relay
from FridgeBot.ArduinoCommunication.TemperatureSensor import TemperatureSensor
from FridgeBot.PiCode.Tasks.FansActions import ActivateFansAction, DeactivateFansAction
from FridgeBot.PiCode.Tasks.RelayActions import ActivateRelayAction, DeactivateRelayAction
from FridgeBot.PiCode.Tasks.FridgeTask import FridgeTask
from FridgeBot.PiCode.Tasks.ScheduleFilter import ScheduleFilter
from FridgeBot.TaskList import TaskList

#Arduino = ArduinoCommunicator("/dev/ttyUSB0")
Arduino = ArduinoCommunicator("COM5")

UV_LIGHT_RELAY = Relay(arduino=Arduino, pin=2, nc=True)
FAN_A = Motor(arduino=Arduino, direction_pin=12, break_pin=9, speed_pin=3)
FAN_B = Motor(arduino=Arduino, direction_pin=13, break_pin=8, speed_pin=11)
TEMPERATURE_SENSOR = TemperatureSensor(arduino=Arduino, pin=4)
HUMIDITY_SENSOR = HumiditySensor(arduino=Arduino, pin=5)

UV_ON_TIME = 20
UV_OFF_TIME = 30
UV_TURN_ON_OFFSET = UV_ON_TIME
UV_TURN_OFF_OFFSET = UV_TURN_ON_OFFSET + UV_OFF_TIME

FANS_TURN_ON_OFFSET = 10
FANS_TURN_OFF_OFFSET = UV_TURN_ON_OFFSET + 20

Tasks = TaskList([
    # TODO: FIX the timing here somehow
    FridgeTask(filter=ScheduleFilter(time_offset=UV_TURN_ON_OFFSET,
                                     restart_cooldown=UV_TURN_OFF_OFFSET - UV_TURN_ON_OFFSET),
               action=ActivateRelayAction(relay=UV_LIGHT_RELAY)),

    FridgeTask(filter=ScheduleFilter(time_offset=UV_TURN_OFF_OFFSET),
               action=DeactivateRelayAction(relay=UV_LIGHT_RELAY)),

    FridgeTask(filter=ScheduleFilter(time_offset=FANS_TURN_ON_OFFSET,
                                     restart_cooldown=FANS_TURN_OFF_OFFSET - FANS_TURN_ON_OFFSET),
               action=ActivateFansAction(fan1=FAN_A, fan2=FAN_B)),

    FridgeTask(filter=ScheduleFilter(time_offset=FANS_TURN_OFF_OFFSET),
               action=DeactivateFansAction(fan1=FAN_A, fan2=FAN_B))
])
