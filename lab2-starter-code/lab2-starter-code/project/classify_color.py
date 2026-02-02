#!/usr/bin/env python3

"""
This test is used to collect data from the color sensor.
It must be run on the robot.
"""

# Add your imports here, if any
from utils.brick import EV3ColorSensor, wait_ready_sensors, TouchSensor, reset_brick


COLOR_SENSOR_DATA_FILE = "../data_analysis/color_sensor.csv"

# complete this based on your hardware setup
COLOR_SENSOR = EV3ColorSensor(2)
TOUCH_SENSOR = TouchSensor(1)

wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.


def collect_color_sensor_data():
    try:
        while True:
            if TouchSensor(1).is_pressed():
                print("Touch Sensor Pressed")
                color_data = COLOR_SENSOR.get_rgb()
                if None not in color_data:
                    print(COLOR_SENSOR.get_rgb())
                    with open(COLOR_SENSOR_DATA_FILE, "w") as output_file:
                        output_file.write(f"{color_data}\n")
    except BaseException:
        pass
    finally:
        print("Done collecting color sensor data")
        reset_brick()
        exit()

if __name__ == "__main__":
    collect_color_sensor_data()
