#!/usr/bin/env python3

"""
Colour Wheel software implementation, main loop
v2.0.0
2026-02-13
"""

# import modules
from time import sleep
from utils import sound
from utils.brick import BP, reset_brick
import math
from classtest import classify
from setup_brickpi import setup_ports
from thumper import drum_setup, drum_iteration

# constants
VERSION = "0.9.1" 
DURATION = 0.3			# seconds, length of each note
VOLUME = 90				# decibels, of speaker
SOUND = sound.Sound(duration=DURATION, pitch="A4", volume=VOLUME)
POLLING_DELAY = 0.1 	# in seconds, for color sensor
COLOR_SENSOR_DATA_FILE = "../data_analysis/classification_data.csv"
NOTES = {"D5":587.33,"G5":783.99, "C5":523.25, "E5":659.25}
COLOURS = {"red":"C5", "purple":"D5", "green":"E5", "orange":"G5"}


def play_sound(pitch):
	"""Play a single note of pitch pitch"""
	SOUND.set_pitch(pitch)
	SOUND.update_audio()
	SOUND.play()
	SOUND.wait_done()

def main_loop(debugging=False, write_to_file=False):
    try:
        played = False      # flag to only play audio once per click
        # set drum parameters
        direction, toggled_yet, drum_on = drum_setup(motor=MOTOR, debugging=debugging)
		# for a posteriori debugging
        if write_to_file:
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
                    try:
                        note = NOTES[COLOURS[classify(color_data)]]
                        print(f"playing note {note}")
                        play_sound(note)
                        if write_to_file:
                        	output_file.write(f"{color_data}\t{note}\n")
                    except:
                        print("INVALID INPUT")
                    finally:
                        played = True
            else:
                # reset flag
                played = False
            # update drum
            direction, toggled_yet, drum_on = drum_iteration(
                    stop = EMERGENCY_STOP,
                    drum_button = US_SENSOR,
                    motor = MOTOR,
                    direction = direction,
                    toggled_yet = toggled_yet,
                    drum_on = drum_on,
                    debugging = debugging
                    )
            sleep(POLLING_DELAY)
        if write_to_file:
        	output_file.close()
        raise Exception("EMERGENCY STOP ACTIVATED")
    except Exception as e:
        # print error message for debugging
        if debugging:
            print("Error: ", e)
    finally:
        print("Powering down...")
        # close file for memory safety
        if write_to_file:
        	output_file.close()
        # reset brick and exit
        reset_brick()
        exit()


if __name__=='__main__':
    TOUCH_SENSOR, COLOR_SENSOR, EMERGENCY_STOP, US_SENSOR, MOTOR = setup_ports(
            play_button=True,
            emergency_stop=True,
            color_sensor=True,
            us_sensor=True,
            drum_motor=True
        )
    print(f"\n\nWelcome to Colour Wheel v{VERSION}")
    print("Turn the wheel to select a note, then play it by pressing the button!")
    print("Use the ultrasonic sensor as a button to toggle the drum on/off")
    print("The emergency stop button can be used to shut down the system")
    main_loop(debugging=True)
    print("Powered down.")
