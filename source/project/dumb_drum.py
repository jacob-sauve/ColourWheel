from utils.brick import Motor, TouchSensor, wait_ready_sensors, reset_brick
import time
from setup_brickpi import setup_ports

STOP, motor = setup_ports(emergency_stop=True, drum_motor=True)

# Designates to Encoder, that the current physical position is 0 degrees
motor.reset_encoder()

# Prevents position control from going over either:
# 50% power or 90 deg/sec, whichever is slower
motor.set_limits(power=80, dps=360)

#motor.set_limits() # UNLIMITED POWER (AND SPEED)

# Will rotate 10 degrees backwards from current position.
# Does not care about the absolute position.
while not STOP.is_pressed():
    motor.set_position_relative(90)
    time.sleep(0.4)
    motor.set_position_relative(-90)
    time.sleep(0.4)

print("Stopped")
reset_brick()
exit()

