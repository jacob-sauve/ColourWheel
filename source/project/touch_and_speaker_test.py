#!/usr/bin/env python3

"""
Module to play sounds when the touch sensor is pressed.
Modified to also allow for soundless touch sensor reliability testing
(i.e., ensure every press is received)
"""

# import modules
from utils import sound
from utils.brick import TouchSensor, wait_ready_sensors

# constants
SOUND = sound.Sound(duration=0.3, pitch="A4", volume=60)


def play_sound():
    """Play a single note."""
    SOUND.play()
    SOUND.wait_done()


def play_sound_on_button_press(testing_speaker=False):
    """In an infinite loop, play a single note when the touch sensor is pressed."""
    n_clicks = 0 # count number of clicks
    message_printed = False # flag to register one click per press even if button held down
    try:
        while True:
            touch_sensor_pressed = TOUCH_SENSOR.is_pressed()
            if touch_sensor_pressed:
                if not message_printed: 
                    message_printed = True
                    n_clicks += 1
                    print(f"Pressed x{n_clicks}")
                if testing_speaker:
                    play_sound()
            else:
                # reset flag on button release
                message_printed = False
    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        exit()


if __name__=='__main__':
    from setup_brickpi import setup_ports
    TOUCH_SENSOR = setup_ports(play_button=True)
    
    print("Playing test tone...")
    play_sound() # beep to indicate entry into program
    
    while True:
        # get user to select testing mode
        choice = input("Choose test sound or test reliability (s/r): ").strip().lower()[0] 
        if (choice == "s"):
            print("Testing sound") 
            play_sound_on_button_press(testing_speaker=True)
        elif (choice == "r"):
            print("Testing reliability") 
            play_sound_on_button_press(testing_speaker=False)
        else:
            print("Invalid input. Please input s or r") 
