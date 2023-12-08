from pololu_3pi_2040_robot import robot

buzzer = robot.Buzzer()
display = robot.Display()

def play():
    intro = "t240 cccagf+lc4 cccagf+ld4 cccbag>c>c>c>c>d>cbf+ld4"
    buzzer.play(intro)