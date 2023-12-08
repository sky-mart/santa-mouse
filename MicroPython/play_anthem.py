from pololu_3pi_2040_robot import robot

buzzer = robot.Buzzer()
display = robot.Display()

def play():
    intro = "t240 v10 cccagfc8 cccagfd8 cccbag>c>c>c>c>d>cbfd8"
    buzzer.play(intro)