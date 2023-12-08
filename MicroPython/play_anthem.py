from pololu_3pi_2040_robot import robot

buzzer = robot.Buzzer()
display = robot.Display()

def play():
    intro = "t140 l2 v10 msc8c8c8a8g8f8mc msc8c8c8a8g8f8 l2md ms8c8c8c8b8a8g8>c8>c8>c8>c8>d8>c8b8g8m2f"
    intro = "t140 l2 v10 b -b b- b b8 b16 b32 b2 b1"
    buzzer.play(intro)