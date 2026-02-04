#!/usr/bin/env python3

"""
Colour Wheel software implementation
v0.5
"""

# import modules
from time import sleep
from utils import sound
from utils.brick import TouchSensor, wait_ready_sensors, BP, EV3ColorSensor, reset_brick

# constants
VERSION = 0.5
DURATION = 0.3
VOLUME = 90
SOUND = sound.Sound(duration=DURATION, pitch="A4", volume=VOLUME)
    # connect TouchSensor to port 1 and ColorSensor to port 2
TOUCH_SENSOR = TouchSensor(1)
COLOR_SENSOR = EV3ColorSensor(2)
EMERGENCY_STOP = TouchSensor(3)
COLOR_SENSOR_DATA_FILE = "../data_analysis/classification_data.csv"
COLOURS = {"A4":440.0, "C4":261.63}

# wait for EV3ColorSensor to initialise (TouchSensor has no init time)
wait_ready_sensors(True)


def classify(rgb):
	"""Return pitch corresponding to given RGB input. Currently dummy (binary select)"""
	from statistics import mean
	return COLOURS["A4"] if mean(rgb) > 50 else COLOURS["C4"]


def play_sound(pitch):
	"""Play a single note of pitch pitch"""
	SOUND.set_pitch(pitch)
	SOUND.update_audio()
	SOUND.play()
	SOUND.wait_done()

def main_loop(debugging=False):
    try:
        played = False # flag to only play audio once per click
        output_file = open(COLOR_SENSOR_DATA_FILE, "w")
        output_file.write("color_data\tnote\n")
        while not EMERGENCY_STOP.is_pressed():
            is_pressed = TOUCH_SENSOR.is_pressed()
            color_data = COLOR_SENSOR.get_rgb()
            if is_pressed:
                if not played:
                    # only register click if not already done for this
                    # button-press
                    if debugging:
                        # additional print debugging if in debug mode
                        print("touch sensor pressed")
                        print(f"{color_data=}")
                    if None not in color_data:
                        note = classify(color_data)
                        print(f"playing note {note}")
                        play_sound(note)
                        output_file.write(f"{color_data}\t{note}\n")
                    played = True
            else:
                # reset flag
                played = False
            sleep(0.1)
        raise Exception("EMERGENCY STOP ACTIVATED")
    except Exception as e:
        # print error message for debugging
        if debugging:
            print("Error: ", e)
    finally:
        print("Powering down...")
        # close file for memory safety
        output_file.close()
        # reset brick and exit
        reset_brick()
        exit()


if __name__=='__main__':
    print(f"\n\nWelcome to Colour Wheel v{VERSION}")
    print("Turn the wheel to select a note, then play it by pressing the button")
    main_loop(debugging=True)
    print("Powered down.")
