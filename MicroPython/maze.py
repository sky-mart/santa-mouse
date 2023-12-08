from pololu_3pi_2040_robot import robot
from pololu_3pi_2040_robot.extras import editions
from machine import Pin
import time
import _thread
import play_anthem

buzzer = robot.Buzzer()
display = robot.Display()
motors = robot.Motors()
line_sensors = robot.LineSensors()

#play_anthem.play()

# Note: It's not safe to use Button B in a
# multi-core program.
button_a = robot.ButtonA()
myselections= ["mode1"]
edition = editions.select_new(myselections)
if edition == "mode1":
    max_speed = 1000
    calibration_speed = 1000
    calibration_count = 100
elif edition == "mode2":
    max_speed = 1000
    calibration_speed = 1000
    calibration_count = 100