#!/usr/bin/env python3

"""
 ______  __  __  __  __           ____    ____    ____
/\__  _\/\ \/\ \/\ \/\ \  /'\_/`\/\  _`\ /\  _`\ /\  _`\
\/_/\ \/\ \ \_\ \ \ \ \ \/\      \ \ \L\ \ \ \L\_\ \ \L\ \
   \ \ \ \ \  _  \ \ \ \ \ \ \__\ \ \ ,__/\ \  _\L\ \ ,  /
    \ \ \ \ \ \ \ \ \ \_\ \ \ \_/\ \ \ \/  \ \ \L\ \ \ \\ \
     \ \_\ \ \_\ \_\ \_____\ \_\\ \_\ \_\   \ \____/\ \_\ \_\
      \/_/  \/_/\/_/\/_____/\/_/ \/_/\/_/    \/___/  \/_/\/ /
Code to control motor for mechanical drum; for use in main loop.
The drum is toggled on/off by pressing a "button" (US sensor).
v 2.0
2026-02-13
"""

# imports
from utils.brick import Motor, TouchSensor
import time

# constants
INSTRUCTION_BUFFER = 0.15   # seconds, nonzero so motor doesn't die. Also counts as US polling buffer
POWER = 80                  # percent, maximum
DPS = 360                   # degrees per second, maximum
US_TRIGGER_DISTANCE = 2     # centimetres, maximal distance for US sensor to detect "press"


def is_pressed(us_sensor, debugging=False):
    """returns True if pressed (i.e. covered), False otherwise or if error occurs"""
    try:
        distance = us_sensor.get_value()
        if debugging:
            print(f"{distance=}")
        if distance < US_TRIGGER_DISTANCE:
            return True
        return False
    except:
        if debugging:
            print("INVALID INPUT")
        return False


def drum_loop(stop, drum_button, motor, debugging=False):
    """runs drum when toggled by US sensor and while emergency stop not pressed"""
    # Designates to Encoder, that the current physical position is 0 degrees
    motor.reset_encoder()

    # Prevents position control from going over either:
    # 80% power or 360 deg/sec, whichever is slower
    motor.set_limits(power=POWER, dps=DPS)

    direction = +1
    toggled_yet = False     # flag to only toggle state once per button press
    drum_on = False
    # run until emergency stop is actuated
    while not stop.is_pressed():
        pressed = is_pressed(drum_button, debugging=debugging)
        if pressed:
            if not toggled_yet:
                # only register click once per button-press
                drum_on = not drum_on
                if debugging:
                    print(f"us sensor 'pressed'; toggling drum state to {drum_on}")
                toggled_yet = True
        else:
            # reset flag
            toggled_yet = False
        
        # run drum if toggled
        if drum_on:
            # added direction to have emergency stop + US sensor verification twice as frequently
            motor.set_position_relative(direction * 90)
            direction *= -1
        # wait outside loop to not overload US sensor when not drumming
        time.sleep(INSTRUCTION_BUFFER)

def drum_setup(motor, power=POWER, dps=DPS, debugging=False):
    """setup already initialized drum stored in variable motor"""
    # indicate to encoder that current pos is 0 degrees
    motor.reset_encoder()
    # max out at the slowest between power% power and dps deg/sec
    motor.set_limits(power=POWER, dps=DPS)
    direction, toggled_yet, drum_on = +1, False, False
    if debugging:
        print(""" ______  __  __  __  __           ____    ____    ____
/\__  _\/\ \/\ \/\ \/\ \  /'\_/`\/\  _`\ /\  _`\ /\  _`\
\/_/\ \/\ \ \_\ \ \ \ \ \/\      \ \ \L\ \ \ \L\_\ \ \L\ \
   \ \ \ \ \  _  \ \ \ \ \ \ \__\ \ \ ,__/\ \  _\L\ \ ,  /
    \ \ \ \ \ \ \ \ \ \_\ \ \ \_/\ \ \ \/  \ \ \L\ \ \ \\ \
     \ \_\ \ \_\ \_\ \_____\ \_\\ \_\ \_\   \ \____/\ \_\ \_\
      \/_/  \/_/\/_/\/_____/\/_/ \/_/\/_/    \/___/  \/_/\/ /"""+ "\n\n... initialised successfully.")
    return direction, toggled_yet, drum_on


def drum_iteration(stop, drum_button, motor, direction, toggled_yet, drum_on, debugging=False, extra_delay=0):
    """single iteration of drum_loop, for integration with colour_wheel_main.py"""
    pressed = is_pressed(drum_button, debugging=debugging)
    if pressed:
        if not toggled_yet:
            # only register click once per button-press
            drum_on = not drum_on
            if debugging:
                print(f"us sensor 'pressed'; toggling drum state to {drum_on}")
            toggled_yet = Trye
        else:
            # reset flag
            toggled_yet = False
    
    # run drum if toggled:
    if drum_on:
        # added direction to have emergency stop + US sensor verification 2x more frequently
        motor.set_position_relative(direction * 90)
        direction  *= -1        # swing opposite way
    # wait outside loop to not overload US sensor when not drumming, only if main loop has insufficient delay
    time.sleep(extra_delay)
    return direction, toggled_yet, drum_on
    

if __name__ == "__main__":
    # for self-contained testing
    from setup_brickpi import setup_ports
    from utils.brickpi import reset_brick

    stop, drum_button, motor = setup_ports(emergency_stop=True, us_sensor=True, drum_motor=True)
    
    try:
        drum_loop(stop, drum_button, motor, debugging=True)
    finally:
        print("Stopped")
        reset_brick()
        exit()
