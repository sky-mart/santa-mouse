from pololu_3pi_2040_robot import robot
from pololu_3pi_2040_robot.extras import editions
from machine import Pin
import time
from array import array
import _thread
import play_anthem

motors = robot.Motors()
bump_sensors = robot.BumpSensors()
line_sensors = robot.LineSensors()
buzzer = robot.Buzzer()
display = robot.Display()
yellow_led = robot.YellowLED()

class MazeSolver:
    def __init__(self, distance_sensor, motor_controller, threshold=5):
        self.history = []
        self.moving_back = False
        self.distance_senstor = distance_sensor
        self.motor_controller = motor_controller
        self.threshold = threshold

    def maze_algo_step():
        forward_move_available = self.distance_sensor.forward_distance() > self.threshold
        left_turn_available = self.distance_sensor.left_distance() > self.threshold;
        right_turn_available = self.distance_sensor.right_distance() > self.threshold
        crossroads = False

        if forward_move_available:
            if left_turn_available or right_turn_available:
                crossroads = True
        else:
            if left_turn_available and right_turn_available:
                crossroads = True

        if not crossroads:
            if forward_move_available:
                motor_controller.move_forward()
            elif left_turn_available:
                motor_controller.turn_left()
                motor_controller.move_forward()
            elif right_turn_available:
                motor_controller.turn_right()
                motor_controller.move_forward()
            else:
                # deadend
                motor_controller.turn_back()
                moving_back = True
                motor_controller.move_forward()
        elif not moving_back:
            if forward_move_available:
                self.history.append(('F'))
                motor_controller.move_forward()
            elif left_turn_available:
                self.history.append(('L'))
                motor_controller.turn_left()
                motor_controller.move_forward()
            elif right_turn_available:
                self.history.append(('R'))
                motor_controller.turn_right()
                motor_controller.move_forward()
            else:
                # deadend
                motor_controller.turn_back()
                moving_back = True
                motor_controller.move_forward()
        else:
            if forward_move_available and 'F' not in self.history[-1]:
                self.history[-1] += ('F')
                motor_controller.moving_back = False
                motor_controller.move_forward()
            elif left_turn_available and 'R' not in self.history[-1]:
                self.history[-1] += ('R')
                moving_back = False
                motor_controller.turn_left()
                motor_controller.move_forward()
            elif right_turn_available and 'L' not in self.history[-1]:
                self.history[-1] += ('L')
                moving_back = False
                motor_controller.turn_right()
                motor_controller.move_forward()
            else:
                # we've checked all variants for this crossroads
                crossroads_self.history.pop_back()

                last_direction = self.history[-1][-1]
                if last_direction == 'F':
                    motor_controller.move_forward()
                elif last_direction == 'L':
                    motor_controller.turn_right()
                    motor_controller.move_forward()
                elif last_direction == 'R':
                    motor_controller.turn_left()
                    motor_controller.move_forward()


#Calibration function
def calibrate_line_sensor():
    time.sleep_ms(500)

    motors.set_speeds(calibration_speed, -calibration_speed)
    for i in range(calibration_count/4):
        line_sensors.calibrate()

    motors.off()
    time.sleep_ms(200)

    motors.set_speeds(-calibration_speed, calibration_speed)
    for i in range(calibration_count/2):
        line_sensors.calibrate()

    motors.off()
    time.sleep_ms(200)

    motors.set_speeds(calibration_speed, -calibration_speed)
    for i in range(calibration_count/4):
        line_sensors.calibrate()

    motors.off()
    time.sleep_ms(200)

def set_calibration_line_sensor():
    min_cal=array('H', [0,0,0,0])
    max_cal=array('H', [1025, 1025, 1025, 1025, 1025])
    line_sensors.set_calibration(min_cal,max_cal)

def check_end():
    #### check if black line is seen

    # save a COPY of the line sensor data in a global variable
    # to allow the other thread to read it safely.
    line = line_sensors.read_calibrated()[:]
    line_sensors.start_read()

    threshold = 600

    if line[0] > threshold and line[1] > threshold and line[3] > threshold and line[4] > threshold:
        display.fill(0)
        display.text("End reached"+str(max_speed),0,20)
        display.text("",0,30)
        display.text("",0,40)
        display.show()
        motors.set_speeds(0, 0)
        motors.off()
        return True
    return False

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
elif edition == "mode3":
    max_speed = 2000
    calibration_speed = 1000
    calibration_count = 100
    turn_time = 250

display.fill(0)
display.text("max speed"+str(max_speed),0,20)
display.text("",0,30)
display.text("",0,40)
display.show()

bump_sensors.calibrate()
display.fill(0)
display.text("bump sensor calibrated",0,20)
display.show()

#line_sensors.calibrate()
#calibrate_line_sensor()
set_calibration_line_sensor()
display.fill(0)
display.text("line sensor calibrated",0,20)
display.show()


display.fill(0)
display.text("start routine",0,20)
display.show()

while True:
    display.fill(0)
    display.text("max speed"+str(max_speed),0,20)
    display.text("",0,30)
    display.text("",0,40)
    display.show()

    motors.set_speeds(max_speed, max_speed)
    bump_sensors.read()

    # break when end is reached
    if check_end():
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
