#!/usr/bin/env python3

"""
Setup the BrickPi sensors
"""

# import modules
from utils.brick import TouchSensor, wait_ready_sensors, EV3UltrasonicSensor, EV3ColorSensor

# constants
PLAY_BUTTON = 1         # for flute actuation
COLOR_SENSOR = 2
EMERGENCY_STOP = 3
US_SENSOR = 4           # drum button


def setup_sensors(play_button=False, color_sensor=False, emergency_stop=False, us_sensor=False):
    """Connect sensors to standard ports"""
    sensors = list()
    if play_button:
        sensors.append(TouchSensor(PLAY_BUTTON))
    if color_sensor:
        sensors.append(EV3ColorSensor(COLOR_SENSOR))
    if emergency_stop:
        sensors.append(TouchSensor(EMERGENCY_STOP))
    if us_sensor:
        sensors.append(EV3UltrasonicSensor(US_SENSOR))
    wait_ready_sensors(True)
    return sensors
