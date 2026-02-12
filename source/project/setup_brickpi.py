#!/usr/bin/env python3

"""
Setup the BrickPi sensors & actuator
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
    """
    Connect sensors and motor to standard ports
    Output order: play_button, color_sensor, emergency_stop, us_sensor, drum_motor
    """
    ports = list()
    print("Connect the following:")
    if play_button:
        print(f"\t*play button (touch) to port S{PLAY_BUTTON}")
        ports.append(TouchSensor(PLAY_BUTTON))
    if color_sensor:
        print(f"\t*color sensor to port S{COLOR_SENSOR}")
        ports.append(EV3ColorSensor(COLOR_SENSOR))
    if emergency_stop:
        print(f"\t*emergency stop (touch) to port S{EMERGENCY_STOP}")
        ports.append(TouchSensor(EMERGENCY_STOP))
    if us_sensor:
        print(f"\t*drum button (US) to port S{US_SENSOR}")
        ports.append(EV3UltrasonicSensor(US_SENSOR))
    if drum_motor:
        print(f"\t*drum motor to port M{DRUM_MOTOR}")
        ports.append(Motor(DRUM_MOTOR))
    wait_ready_sensors(True)
    return ports
