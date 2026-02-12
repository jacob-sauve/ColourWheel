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


def fix(dataset, output_filepath):
    """Remove outliers from 1D dataset, return mean without outliers, write data points to filepath"""
    raw_mean = mean(dataset)
    raw_sd = stdev(dataset)
    no_outliers = list(dataset)
    for val in dataset:
        if abs(val-mean) > raw_sd:
            no_outliers.remove(val)
    try:
        with open(output_filepath, "w") as file:
            for val in dataset:
                file.write(val)
    except:
        print("file-writing failed")
    return mean(no_outliers)


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
    from setup_brickpi import setup_sensors
    PlAY_BUTTON, COLOR_SENSOR, EMERGENCY_STOP = setup_sensors(play_button=True, color_sensor=True, emergency_stop=True)
    for note in ["C5", "D5", "E5", "G5"]:
        color = input("color name: ")
        calibrate_color(color)

