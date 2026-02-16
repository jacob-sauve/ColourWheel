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
The drum is toggled on by pressing a "button" (US sensor).
v 3.3
2026-02-16
"""

# imports
from utils.brick import Motor, TouchSensor
import time

# constants
INSTRUCTION_BUFFER = 0.05   # seconds, nonzero so motor doesn't die. Also counts as US polling buffer
POWER = 200                 # percent, maximum
DPS = 1000                  # degrees per second, maximum
US_TRIGGER_DISTANCE = 4.0   # centimetres, maximal distance for US sensor to detect "press"
COUNTS_PER_ROTATION = 10    # amount of iterations before direction is reversed
HALF_RANGE_OF_MOTION = 45   # degrees, total range of motion of the drum swing, also how encoder interprets initial position


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


def drum_setup(motor, power=POWER, dps=DPS, debugging=False):
    """setup already initialized drum stored in variable motor"""
    motor.reset_encoder()
    motor.offset_encoder(HALF_RANGE_OF_MOTION - 5)    # have the motor start touching drum
    # max out at the slowest between power% power and dps deg/sec
    motor.set_limits(power=POWER, dps=DPS)
    direction, toggled_yet, drum_on, counter = +1, False, False, COUNTS_PER_ROTATION
    if debugging:
        print("\n\n... initialised successfully.")
    return direction, toggled_yet, drum_on, counter


def drum_iteration(stop, drum_button, motor, direction, toggled_yet, drum_on, counter, debugging=False, extra_delay=0):
    """single iteration of drum_loop, for integration with colour_wheel_main.py"""
    pressed = is_pressed(drum_button, debugging=debugging)
    if pressed:
        if not toggled_yet:
            # only register click once per button-press
            #drum_on = not drum_on
            drum_on = True # removes toggle -zach
            if debugging:
                print(f"us sensor 'pressed'; toggling drum state to {drum_on}")
            toggled_yet = True
        else:
            # reset flag
            toggled_yet = False
    
    # run drum if toggled:
    if drum_on and counter >= COUNTS_PER_ROTATION:
        # added direction to have emergency stop + US sensor verification 2x more frequently
        if debugging:
            print(f"turning {direction} * {HALF_RANGE_OF_MOTION} degrees")
        motor.set_position(direction * HALF_RANGE_OF_MOTION)
        direction  *= -1        # swing opposite way
        counter = 0
    else:
        counter += 1
    # wait outside loop to not overload US sensor when not drumming, only if main loop has insufficient delay
    time.sleep(extra_delay)
    return direction, toggled_yet, drum_on, counter


def drum_loop(stop, drum_button, motor, debugging=False):
    """runs drum when toggled by US sensor and while emergency stop not pressed"""
    direction, toggled_yet, drum_on, counter = drum_setup(motor, debugging=debugging)
    # run until emergency stop is actuated
    while not stop.is_pressed():
        direction, toggled_yet, drum_on, counter = drum_iteration(
            stop,
            drum_button,
            motor,
            direction,
            toggled_yet,
            drum_on,
            counter,
            debugging = debugging,
            extra_delay = INSTRUCTION_BUFFER    # to not overload US sensor or motor
        )


if __name__ == "__main__":
    # for self-contained testing
    from setup_brickpi import setup_ports
    from utils.brick import reset_brick

    stop, drum_button, motor = setup_ports(emergency_stop=True, us_sensor=True, drum_motor=True)
    
    try:
        drum_loop(stop, drum_button, motor, debugging=True)
    finally:
        print("Stopped")
        reset_brick()
        exit()
