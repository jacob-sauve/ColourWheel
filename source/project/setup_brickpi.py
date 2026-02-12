#!/usr/bin/env python3

"""
Standard setup for the BrickPi sensors & actuator
"""

# import modules
from utils.brick import TouchSensor, wait_ready_sensors, EV3UltrasonicSensor, EV3ColorSensor, Motor

# STANDARD PORTS FOR ALL TESTS + MAIN CODE
# vvv (change here if needed) vvv
PLAY_BUTTON = 1         # for flute actuation
COLOR_SENSOR = 2
EMERGENCY_STOP = 3
US_SENSOR = 4           # drum button
DRUM_MOTOR = "D"        # drum motor 

# master dictionary
port_map = {
    "play_button" : {
        "label" : "play button (touch)",
        "port" : PLAY_BUTTON,
        "function" : TouchSensor
    },
    "color_sensor" : {
        "label" : "color sensor",
        "port" : COLOR_SENSOR,
        "function" : EV3ColorSensor
    },
    "emergency_stop" : {
        "label" : "emergency stop (touch)",
        "port" : EMERGENCY_STOP,
        "function" : TouchSensor
    },
    "us_sensor" : {
        "label" : "drum button (US)",
        "port" : US_SENSOR,
        "function" : EV3UltrasonicSensor
    },
    "drum_motor" : {
        "label" : "drum motor",
        "port" : DRUM_MOTOR, 
        "function" : Motor
    },
}


def setup_ports(play_button=False, color_sensor=False, emergency_stop=False, us_sensor=False, drum_motor=False, verbose=True):
    """
    Connect sensors and motor to standard ports
    Output order: play_button, color_sensor, emergency_stop, us_sensor, drum_motor
    """
    arg_dict = locals()
    ports = list()
    if verbose:
        print("Connect the following:")
    for varname, flag in arg_dict:
        if varname != "verbose":
            if flag:
                if verbose:
                    print(f"\t*{port_map[varname]["label"]} to port S{port_map[varname]["port"]}")
                ports.append(port_map[varname]["function"](port_map[varname]["port"]))
    wait_ready_sensors(True)
    return ports
