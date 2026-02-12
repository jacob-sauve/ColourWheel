#!/usr/bin/env python3

"""
This test is used to collect data from the color sensor.
It must be run on the robot.
"""

# imported modules
import time
from utils.brick import BP, EV3ColorSensor, wait_ready_sensors, TouchSensor, reset_brick

# constants
COLOR_SENSOR_DATA_FILE = "../data_analysis/color_sensor.csv"


def collect_color_sensor_data():
    try:
        measured = False # flag to only measure once per click
        output_file = open(COLOR_SENSOR_DATA_FILE, "w")
        while True:
            is_pressed = TOUCH_SENSOR.is_pressed()
            color_data = COLOR_SENSOR.get_rgb()
            if is_pressed:
                if not measured:
                    # only register click if not already done for this
                    # button-press
                    print("touch sensor pressed")
                    if color_data is not None:
                        print(color_data)
                        output_file.write(f"{color_data}\n")
                    measured = True
            else:
                # reset flag
                measured = False
            time.sleep(0.1)
    except Exception as e:
        # print error message for debugging
        print("Error: ", e)
    finally:
        print("Done collecting color sensor data")
        # close file for memory safety
        output_file.close()
        # reset brick and exit
        reset_brick()
        exit()

if __name__ == "__main__":
    from setup_brickpi import setup_ports
    TOUCH_SENSOR, COLOR_SENSOR = setup_ports(play_button=True, color_sensor=True)
    collect_color_sensor_data()
