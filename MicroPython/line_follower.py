# PID line follower demo.
#
# Place the robot on the line and press A to calibrate, then press A
# again to start it following the line.  You can also press A later
# to stop the motors.
#
# This demo shows how to use the _thread library to run a fast main
# loop on one core of the RP2040.  The other core is free to run
# slower functions like updating the display without impacting the
# speed of the main loop.

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
led = Pin(25, Pin.OUT)

play_anthem.play()

# Note: It's not safe to use Button B in a
# multi-core program.
button_a = robot.ButtonA()

edition = editions.select()
if edition == "Standard":
    min_speed = 0
    max_speed = 3000
    calibration_speed = 1000
    calibration_count = 100
elif edition == "Turtle":
    min_speed = 0
    max_speed = 2000
    calibration_speed = 1000
    calibration_count = 100
elif edition == "Hyper":
    min_speed = 0
    max_speed = 4000
    calibration_speed = 1000
    calibration_count = 100
    #motors.flip_left(True)
    #motors.flip_right(True)

display.fill(0)
display.text("Line Follower", 0, 0)
display.text("Place on line", 0, 20)
display.text("and press A to", 0, 30)
display.text("calibrate.", 0, 40)
display.show()

# while not button_a.check():
    # pass

display.fill(0)
display.show()
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

t1 = 0
t2 = time.ticks_us()
p = 0
line = []
starting = False
stop = False
run_motors = False
last_update_ms = 0

def update_display():
    display.fill(0)
    if stop:
        display.text("Stop", 0, 0)
        return

    display.text("Line Follower", 0, 0)
    if starting:
        display.text("Press A to stop", 0, 10)
    else:
        display.text("Press A to start", 0, 10)

    ms = (t2 - t1)/1000
    display.text(f"Main loop: {ms:.1f}ms", 0, 20)
    display.text('p = '+str(p), 0, 30)

    # 64-40 = 24
    scale = 24/1000

    print(line)
    display.fill_rect(36, 64-int(line[0]*scale), 8, int(line[0]*scale), 1)
    display.fill_rect(48, 64-int(line[1]*scale), 8, int(line[1]*scale), 1)
    display.fill_rect(60, 64-int(line[2]*scale), 8, int(line[2]*scale), 1)
    display.fill_rect(72, 64-int(line[3]*scale), 8, int(line[3]*scale), 1)
    display.fill_rect(84, 64-int(line[4]*scale), 8, int(line[4]*scale), 1)

    display.show()

def follow_line():
    last_p = 0
    i = 0
    global p, ir, t1, t2, line, max_speed, run_motors, stop, min_speed
    left_turn = False
    right_turn = False
    while True:
        # save a COPY of the line sensor data in a global variable
        # to allow the other thread to read it safely.
        line = line_sensors.read_calibrated()[:]
        line_sensors.start_read()
        t1 = t2
        t2 = time.ticks_us()

        threshold = 600

        if line[0] > threshold and line[1] > threshold and line[3] > threshold and line[4] > threshold:
            stop = True
            motors.set_speeds(0, 0)
            motors.off()
            run_motors = False
            # motors.off()
            # break

        if line[1] < threshold and line[2] < threshold and line[3] < threshold: #Center off the line
            if p < 0: # negative p means robot is to right of line
                l = 1000 #previously 0
            else: # postive p means robot is to left of line
                l = 3000 #previously 4000
        elif line[0] > threshold and line[1] > threshold and line[2] > threshold and line[3] > threshold: #left turn
            left_turn = True
        elif line[1] > threshold and line[2] > threshold and line[3] > threshold and line[4] > threshold: #right turn
            right_turn = True
        else:
            # estimate line position
            l = (1000*line[1] + 2000*line[2] + 3000*line[3] + 4000*line[4]) // \
                sum(line)

        if left_turn:
            motors.set_speeds(0, 0)
            time.sleep_ms(200)
            for i in range(calibration_count/6):
                motors.set_speeds(-calibration_speed, calibration_speed)
        elif right_turn:
            motors.set_speeds(0, 0)
            time.sleep_ms(200)
            for i in range(calibration_count/6):
                motors.set_speeds(calibration_speed, +calibration_speed)
        else:
            p = l - 2000
            i += p
            d = p - last_p
            last_p = p
            pid = p*90 + i*40 + d*2000 #negative = left turn, positve = right turn
            pid = pid * 0.01 #scale down pid

            left = max(min_speed, min(max_speed, max_speed + (pid))) #Split pid per wheel for lesser effect
            right = max(min_speed, min(max_speed, max_speed - (pid)))

        if run_motors:
            if left_turn:
                left_turn = False
            elif right_turn:
                right_turn = False
            else:
                motors.set_speeds(left, right)
        else:
            motors.off()

_thread.start_new_thread(follow_line, ())

while True:
    t = time.ticks_ms()

    if time.ticks_diff(t, last_update_ms) > 100:
        last_update_ms = t
        update_display()

    if button_a.check():
        if not starting:
            starting = True
            start_ms = t
        else:
            starting = False
            run_motors = False

    if not stop and starting and time.ticks_diff(t, start_ms) > 1000:
        run_motors = True
