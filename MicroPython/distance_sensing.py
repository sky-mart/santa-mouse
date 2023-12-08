from pololu_3pi_2040_robot import robot
from machine import I2C, Pin
from vl6180x import Sensor
import time

display = robot.Display()

MAX_DIST_RAW = 190
MIN_DIST_RAW = 10
MAX_DIST_PHY = 20.5
MIN_DIST_PHY = 1.5
RAW_RANGE = 180
PHY_RANGE = 19
FACTOR = 180.0 / 19.0


def dbg(text):
  display.fill(0)
  display.text(text, 0, 0)
  display.show()

def display_measurements(left, mid, right):
  display.fill(0)
  display.text(str(left), 00, 0)
  display.text(str(mid), 20, 0)
  display.text(str(right), 40, 0)
  display.show()


class DistanceSensor:
  def __init__(self, i2c, new_i2c_addr, shutdown_pin):
    shutdown_pin.high();
    i2c.writeto_mem(0x29, 0x212, bytearray([new_i2c_addr]), addrsize=16)
    self.tof = Sensor(i2c, address=new_i2c_addr)

  def get_distance(self):
    time.sleep(0.01)
    actual_value = self.tof.range()
    if actual_value > 190:
      actual_value = 190
    actual_value -= MIN_DIST_RAW
    return (actual_value / FACTOR) + 1.5


class DistanceArray:
  def __init__(self, i2c, shut_pins):
    for shut_pin in shut_pins:
      shut_pin.low()

      self.left = DistanceSensor(i2c, 0x30, shut_pins[0])
      self.mid = DistanceSensor(i2c, 0x31, shut_pins[1])
      self.right = DistanceSensor(i2c, 0x32, shut_pins[2])

  def left_distance(self):
    return self.left.get_distance()

  def mid_distance(self):
    return self.mid.get_distance()

  def right_distance(self):
    return self.right.get_distance()


def main():
  shut_pin_left = Pin(24)
  shut_pin_mid = Pin(7)
  shut_pin_right = Pin(6)

  i2c = I2C(id=0, scl=Pin(5), sda=Pin(4), freq=400_000)

  da = DistanceArray(i2c, [shut_pin_left, shut_pin_mid, shut_pin_right])

  while True:
    display_measurements(da.left_distance(), da.mid_distance(), da.right_distance())


main()
