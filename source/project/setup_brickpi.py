#!/usr/bin/env python3

"""
Setup the BrickPi sensors
"""

# import modules
from utils.brick import TouchSensor, wait_ready_sensors, EV3UltrasonicSensor, EV3ColorSensor, Motor

# constants
PLAY_BUTTON = 1         # for flute actuation
COLOR_SENSOR = 2
EMERGENCY_STOP = 3
US_SENSOR = 4           # drum button
DRUM_MOTOR = "D"        # drum motor 


def setup_ports(play_button=False, color_sensor=False, emergency_stop=False, us_sensor=False, drum_motor=False):
    """Connect sensors and motor to standard ports"""
    ports = list()
    if play_button:
        ports.append(TouchSensor(PLAY_BUTTON))
    if color_sensor:
        ports.append(EV3ColorSensor(COLOR_SENSOR))
    if emergency_stop:
        ports.append(TouchSensor(EMERGENCY_STOP))
    if us_sensor:
        ports.append(EV3UltrasonicSensor(US_SENSOR))
    if drum_motor:
        ports.append(Motor(DRUM_MOTOR))
    wait_ready_sensors(True)
    return ports
