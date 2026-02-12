#!/usr/bin/env python3

"""
This script calibrates the color sensor by collecting profiles of different blocks
For each block:
1. collect raw color profile data points
2. calculate mean and SD
3. remove outliers (+/- >1 SD from mean)
4. calculate and save new representative mean
5. associate to a note
"""

# imported modules
import time
from utils.brick import BP, EV3ColorSensor, wait_ready_sensors, TouchSensor, reset_brick
from classtest import classify
from statistics import mean, stdev

# constants
POLLING_DELAY = 0.1 # seconds
CALIBRATION_DATA_PATH = "../calibration_data/"

# complete this based on your hardware setup
COLOR_SENSOR = EV3ColorSensor(3)
TOUCH_SENSOR = TouchSensor(1)

wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.






def calibrate_color(color):
    try:
        omega_vals = list()
        measured = False # flag to only measure once per click
        output_file = open(f"{CALIBRATION_DATA_PATH}{color}.csv", "w")
        while True:
            is_pressed = TOUCH_SENSOR.is_pressed()
            color_data = COLOR_SENSOR.get_rgb()
            if is_pressed:
                if not measured:
                    # only register click if not already done for this
                    # button-press
                    print("touch sensor pressed")
                    try:
                        print(classify(color_data))
                        output_file.write(f"{classify(color_data)}\n")
                    except:
                        print("Invalid reading - try again")
                    measured = True
            else:
                # reset flag
                measured = False
            time.sleep(POLLING_DELAY) # so as not to kill the color sensor
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
    for note in ["C5", "D5", "E5", "G5"]:
        color = input("color name: ")
        calibrate_color(color)

