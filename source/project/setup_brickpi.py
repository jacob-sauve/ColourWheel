#!/usr/bin/env python3

"""
Standard setup for the BrickPi sensors & actuator
Implemented in all tests and in main code for consistency
v 1.1
2026-02-19
"""

# import modules
from utils.brick import TouchSensor, wait_ready_sensors, EV3UltrasonicSensor, EV3ColorSensor, Motor

# STANDARD PORTS FOR ALL TESTS + MAIN CODE
# vvv (change here if needed) vvv
PLAY_BUTTON = 1         # for flute actuation
COLOR_SENSOR = 2        # for note selection
EMERGENCY_STOP = 3      # E-Stop
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
    """Connect sensors and motor to standard ports
    Keyword arguments:
        play_button     -- flag to initialise a TouchSensor to serve as a flute actuator (default False)
        color_sensor    -- flag to initialise an EV3ColorSensor to serve as note selector (default False)
        emergency_stop  -- flag to initialise a TouchSensor to serve as an emergency stop (default False)
        us_sensor       -- flag to initialise an EV3UltrasonicSensor as a drum 'on button' (default False)
        drum_motor      -- flag to initialise a Motor as the drum's percussor (default False)
        verbose         -- flag to explicitly print debugging and instructional messages regarding port setup (default True)
    Outputs:
        play_button     -- initialised TouchSensor object (if play_button)
        color_sensor    -- initialised EV3ColorSensor object (if color_sensor)
        emergency_stop  -- initialised TouchSensor object (if emergency_stop)
        us_sensor       -- initialised EV3UltrasonicSensor object (if us_sensor)
        drum_motor      -- initialised Motor object (if drum_motor)
    """
    arg_dict = locals()             # create arg:val dictionary
    ports = list()                  # list to hold sensor/actuator objects
    if verbose:
        print("Connect the following:")
    for varname, flag in arg_dict.items():
        if varname != "verbose":    # verbose argument does not correspond to a sensor/actuator
            # initialise each port that is flagged True
            if flag:
                if verbose:
                    print(f"\t*{port_map[varname]['label']} to port {port_map[varname]['port']}")
                ports.append(port_map[varname]["function"](port_map[varname]["port"]))
    wait_ready_sensors(verbose)
    return ports
