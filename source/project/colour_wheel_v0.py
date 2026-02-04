#!/usr/bin/env python3

"""
Colour Wheel software implementation
v0.0
"""

# import modules
from utils import sound
from utils.brick import TouchSensor, wait_ready_sensors
import colour_selection.py as c

# constants
VERSION = 0.0
DURATION = 0.3
VOLUME = 90
SOUND = sound.Sound(duration=DURATION, pitch="A4", volume=VOLUME)
TOUCH_SENSOR = TouchSensor(1)

wait_ready_sensors() # Note: Touch sensors actually have no initialization time


def play_sound(pitch, duration=DURATION, volume=VOLUME):
    """Play a single note."""
    new_sound = sound.Sound(duration=duration, pitch=pitch, volume=volume)
    new_sound.play()
    new_sound.wait_done()


def main_loop():
    """In an infinite loop, play a single note when the touch sensor is pressed."""
    sound_played = False # flag to register one click per press even if button held down
    try:
        note = -1
        while True:
            touch_sensor_pressed = TOUCH_SENSOR.is_pressed()
            new_note = c.note_select()
            if touch_sensor_pressed:
                if not sound_played or new_note != note: 
                    sound_played = True
                    note = new_note
                    print(f"Playing {note}")
                    play_sound(note)
            else:
                # reset flag on button release
                message_printed = False
    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        exit()


if __name__=='__main__':
    print(f"Welcome to Colour Wheel v{VERSION}")
    print("Turn the wheel to select a note, then play it by pressing the button")
    main_loop()
    print("Powering down...")
