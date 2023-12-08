from pololu_3pi_2040_robot import robot

buzzer = robot.Buzzer()
display = robot.Display()

def play():
    intro = "t240 cccagfc4 cccagfd4 cccbagc>c>c>c>d>c>bfd4"
    buzzer.play(intro)