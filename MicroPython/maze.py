from pololu_3pi_2040_robot import robot
from pololu_3pi_2040_robot.extras import editions
from machine import Pin
import time
import _thread
import play_anthem

motors = robot.Motors()
bump_sensors = robot.BumpSensors()
line_sensors = robot.LineSensors()
buzzer = robot.Buzzer()
display = robot.Display()
yellow_led = robot.YellowLED()

#play_anthem.play()

# Note: It's not safe to use Button B in a
# multi-core program.
button_a = robot.ButtonA()
myselections= ["mode1", "mode2", "mode3"]
edition = editions.select_new(myselections)
if edition == "mode1":
    max_speed = 1000
    calibration_speed = 1000
    calibration_count = 100
    turn_time = 250
elif edition == "mode2":
    max_speed = 1500
    calibration_speed = 1000
    calibration_count = 100
    turn_time = 250
elif edition == "mode2":
    max_speed = 2000
    calibration_speed = 1000
    calibration_count = 100
    turn_time = 250

display.fill(0)
display.show()

bump_sensors.calibrate()
display.text("bump sensor calibrated")
display.show()

line_sensors.calibrate()
display.text("line sensor calibrated")
display.show()

time.sleep_ms(1000)

def check_end():
    #### check if black line is seen

    # save a COPY of the line sensor data in a global variable
    # to allow the other thread to read it safely.
    line = line_sensors.read_calibrated()[:]
    line_sensors.start_read()

    threshold = 600

    if line[0] > threshold and line[1] > threshold and line[3] > threshold and line[4] > threshold:
        motors.set_speeds(0, 0)
        motors.off()
        return True

display.text("start routine")
display.show()


while True:
    motors.set_speeds(max_speed, max_speed)
    bump_sensors.read()
    
    # break when end is reached
    if check_end:
        break

    if bump_sensors.left_is_pressed():
        yellow_led.on()
        motors.set_speeds(0, 0)
        buzzer.play("a32")
        display.fill(0)
        display.text("Left", 0, 0)
        display.show()

        motors.set_speeds(max_speed, -max_speed)
        time.sleep_ms(turn_time)

        motors.set_speeds(0, 0)
        buzzer.play("b32")
        yellow_led.off()

        display.fill(0)
        display.show()

    if bump_sensors.right_is_pressed():
        yellow_led.on()
        motors.set_speeds(0, 0)
        buzzer.play("e32")
        display.fill(0)
        display.text("Right", 88, 0)
        display.show()

        motors.set_speeds(-max_speed, max_speed)
        time.sleep_ms(turn_time)

        motors.set_speeds(0, 0)
        buzzer.play("f32")
        yellow_led.off()

        display.fill(0)
        display.show()    