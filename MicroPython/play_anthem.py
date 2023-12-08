from pololu_3pi_2040_robot import robot

buzzer = robot.Buzzer()
display = robot.Display()

def play():
    intro = "t240 v10 cccagf+c8 cccagf+d8 cccbag>c>c>c>c>d>cbf+d8"
    buzzer.play(intro)