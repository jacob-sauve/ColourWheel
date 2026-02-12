#!/usr/bin/env python3

"""
This test is used to collect hue-adjacent values ("omega" values) for a brick.
"""

# imported modules
import time
from utils.brick import BP, EV3ColorSensor, TouchSensor, reset_brick
from classtest import classify

# constants
COLOR_SENSOR_DATA_FILE = "../data_analysis/omega_values.csv"


def collect_brick_omega_values(color_sensor, touch_sensor):
    try:
        measured = False # flag to only measure once per click
        output_file = open(COLOR_SENSOR_DATA_FILE, "w")
        while True:
            is_pressed = touch_sensor.is_pressed()
            color_data = color_sensor.get_rgb()
            if is_pressed:
                if not measured:
                    # only register click if not already done for this
                    # button-press
                    print("touch sensor pressed")
                    if color_data is not None:
                        try:
                            print(classify(color_data))
                            output_file.write(f"{classify(color_data)}\n")
                        except:
                            print("Invalid reading - try again")
                    else:
                        print("Invalid reading - try again")
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
    collect_brick_omega_values(COLOR_SENSOR, TOUCH_SENSOR)
