from pololu_3pi_2040_robot import robot

buzzer = robot.Buzzer()
display = robot.Display()

def play():
    intro = "t240 cccagf+lc8 cccagf+ld8 cccbag>c>c>c>c>d>cbf+ld8"
    buzzer.play(intro)