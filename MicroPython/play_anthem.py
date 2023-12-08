from pololu_3pi_2040_robot import robot

buzzer = robot.Buzzer()
display = robot.Display()

def play():
    intro = "t240 l16 v10 cccagfc4 cccagfdddd cccbag>c>c>c>c>d>cbgf32"
    buzzer.play(intro)