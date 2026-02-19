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
v 3.4
2026-02-19
"""

# imports
from utils.brick import Motor, TouchSensor
import time

# constants
INSTRUCTION_BUFFER = 0.05   # seconds, nonzero so motor doesn't die. Also counts as US Sensor polling buffer
POWER = 200                 # percent, maximum power
DPS = 1000                  # degrees per second, maximum speed
US_TRIGGER_DISTANCE = 4.0   # centimetres, maximal distance for US sensor to detect "press"
COUNTS_PER_ROTATION = 10    # amount of iterations of main loop before drum direction is reversed
HALF_RANGE_OF_MOTION = 45   # degrees, half range of motion of the drum swing, also how encoder interprets initial position


def is_pressed(us_sensor, debugging=False):
    """Returns True if 'button' pressed (i.e. covered), False otherwise or if error occurs
    Keyword arguments:
        us_sensor   -- the EV3UltrasonicSensor object being used as a button
        debugging   -- flag to toggle informative print statements on/off when True/False (default False)
    """
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
    """Setup motor with correct parameters to be a drum
    Keyword arguments:
        motor       -- the Motor object which acts as the drum
        power       -- maximum motor power in percentage (default POWER)
        dps         -- maximum motor speed in degrees per second (default DPS)
        debugging   -- flag to toggle informative print statements on/off when True/False (default False)
    Output:
        direction   -- initial value of direction (see drum_iteration), +1
        drum_on     -- initial value of drum_on (see drum_iteration), False
        counter     -- initial value of counter (see drum_iteration), COUNTS_PER_ROTATION
        """
    motor.reset_encoder()
    motor.offset_encoder(HALF_RANGE_OF_MOTION - 5)    # have the motor start touching drum
    # max out at the slowest between power% power and dps deg/sec
    motor.set_limits(power=POWER, dps=DPS)
    direction, drum_on, counter = +1, False, COUNTS_PER_ROTATION
    if debugging:
        print("\n\n... initialised successfully.")
    return direction, drum_on, counter


def drum_iteration(drum_button, motor, direction, drum_on, counter, debugging=False, extra_delay=0):
    """Single iteration of drum_loop, for integration with colour_wheel_main.py
    Keyword arguments:
        drum_button -- the EV3UltrasonicSensor object which triggers the drum
        motor       -- the Motor object which acts as the drum
        direction   -- makes Motor turn clockwise when positive, counterclockwise when negative
        drum_on     -- False until drum has been turned on, then True to stop US Sensor polling and start drum
        counter     -- multithreading substitute, counts iterations of main loop before drum direction update
        debugging   -- flag to toggle informative print statements on/off when True/False (default False)
        extra_delay -- delay (in seconds) added after each call of drum_iteration (default 0)
    Output:
        direction   -- updated value of direction
        drum_on     -- updated value of drum_on
        counter     -- updated value of counter
        """
    # only check first US sensor press
    if not drum_on:
        pressed = is_pressed(drum_button, debugging=debugging)
        if pressed:
            drum_on = True
            if debugging:
                print(f"us sensor 'pressed'; toggling drum state to {drum_on}")
    
    # run drum if toggled AND only once per COUNTS_PER_ROTATION iterations
    if drum_on and counter >= COUNTS_PER_ROTATION:
        # added direction to have emergency stop + US sensor verification 2x more frequently
        if debugging:
            print(f"turning {direction} * {HALF_RANGE_OF_MOTION} degrees")
        motor.set_position(direction * HALF_RANGE_OF_MOTION)
        direction  *= -1        # swing opposite way
        counter = 0
    else:
        counter += 1
    # wait outside loop to not overload US sensor even when not drumming, only if main loop has insufficient delay
    time.sleep(extra_delay)
    return direction, drum_on, counter


def drum_loop(stop, drum_button, motor, debugging=False):
    """Testing loop that runs drum after turned on by US Sensor and while emergency stop not pressed
    Keyword arguments:
        stop        -- the TouchSensor object being used as an emergency stop button
        drum_button -- the EV3UltrasonicSensor object which triggers the drum
        motor       -- the Motor object which acts as the drum
        debugging   -- flag to toggle informative print statements on/off when True/False (default False)
    """
    direction, drum_on, counter = drum_setup(motor, debugging=debugging)
    # run until emergency stop is actuated
    while not stop.is_pressed():
        # update drum state
        direction, drum_on, counter = drum_iteration(
            drum_button,
            motor,
            direction,
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
