#!/usr/bin/env python3

"""
This test is used to collect data from the color sensor.
It must be run on the robot.
"""

# Add your imports here, if any
import time
from utils.brick import BP, EV3ColorSensor, wait_ready_sensors, TouchSensor, reset_brick


COLOR_SENSOR_DATA_FILE = "../data_analysis/color_sensor.csv"

# complete this based on your hardware setup
COLOR_SENSOR = EV3ColorSensor(3)
TOUCH_SENSOR = TouchSensor(1)

#COLOR_SENSOR.set_mode("rgb")

wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.

def collect_color_sensor_data():
    try:
        measured = False # flag to only measure once per click
        output_file = open(COLOR_SENSOR_DATA_FILE, "w")
        while True:
            is_pressed = TOUCH_SENSOR.is_pressed()
            color_data = COLOR_SENSOR.get_rgb()
            if is_pressed:
                if not measured:
                    print("touch sensor pressed")
                    if color_data is not None:
                        print(color_data)
                        output_file.write(f"{color_data}\n")
                    measured = True
            else:
                measured = False
            time.sleep(0.1)
#                if not measured:
#                    measured = True
#                    print("Touch Sensor Pressed")
#                    color_data = COLOR_SENSOR.get_rgb()
#                    if None not in color_data:
#                        print(color_data)
#                        output_file.write(f"{color_data}\n")
#                        with open(COLOR_SENSOR_DATA_FILE, "a") as output_file:
#                            output_file.write(f"{color_data}\n")
#                            output_file.close()
#            else:
#                measured = False
    except Exception as e:
        print("Error: ", e)
    finally:
        print("Done collecting color sensor data")
        output_file.close()
        reset_brick()
        exit()

if __name__ == "__main__":
    collect_color_sensor_data()
