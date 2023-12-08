from pololu_3pi_2040_robot import robot

buzzer = robot.Buzzer()
display = robot.Display()

def play():
    intro = "t140 l2 v10 ms2c8c8c8a8g8f8m2c msc8c8c8a8g8f8md ms8c8c8c8b8a8g8>c8>c8>c8>c8>d8>c8-b8g8m2f"
    buzzer.play(intro)