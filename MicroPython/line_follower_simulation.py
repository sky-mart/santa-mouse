def follow_line():
    last_p = 0
    global p, ir, t1, t2, line, max_speed, run_motors, stop

    max_speed = 6000
    # save a COPY of the line sensor data in a global variable
    # to allow the other thread to read it safely.
    line = [500, 800, 700, 800, 300]

    threshold = 600

    # postive p means robot is to left of line
    if line[1] < threshold and line[2] < threshold and line[3] < threshold: #Center off the line
        if p < 0:
            l = 1000
        else:
            l = 3000 
    else:
        # estimate line position
        l = (1000*line[1] + 2000*line[2] + 3000*line[3] + 4000*line[4]) // \
            sum(line)

    p = l - 2000
    d = p - last_p
    last_p = p
    pid = p*90 + d*200 # negative = left turn, positve = right turn

    min_speed = 0
    left = max(min_speed, min(max_speed, max_speed + pid))
    right = max(min_speed, min(max_speed, max_speed - pid))

    print(l)
    print(p)
    print(pid*0.1)
    print(left, right)

follow_line()