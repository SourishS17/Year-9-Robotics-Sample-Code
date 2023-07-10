# commit as main2.py
# T junctions now work, corners in functions, slightly longer forward on straight lines.
from machine import Pin, PWM
from time import sleep, time

sensor_middle = Pin(21, Pin.IN)
sensor_left = Pin(20, Pin.IN)
sensor_right = Pin(22, Pin.IN)
in1 = Pin(14, Pin.OUT)
in2 = Pin(13, Pin.OUT)
in3 = Pin(11, Pin.OUT)
in4 = Pin(10, Pin.OUT)

lost = False

speedControl1 = PWM(Pin(1))S
speedControl2 = PWM(Pin(2))
 
speedControl2.freq(1000)
speedControl2.duty_u16(50000)

speedControl1.freq(1000)
speedControl1.duty_u16(50000)

def forwards():
    in1.value(1)
    in2.value(0)
    in3.value(1)
    in4.value(0)

def right():    
    in1.value(1)
    in2.value(0)
    in3.value(0)
    in4.value(1)
    
def left():    
    in1.value(0)
    in2.value(1)
    in3.value(1)
    in4.value(0)
    
def pause():
    in1.value(0)
    in2.value(0)
    in3.value(0)
    in4.value(0)

def read():
    global val1
    global val2
    global val3
    val1 = sensor_right.value()
    val2 = sensor_middle.value()
    val3 = sensor_left.value()
    
def left_turn():
    global val1
    global val2
    global val3
    #If approaching from an angle, needs to check for T
    count = 0
    while count <= 3:
        read()
        forwards()
        sleep(0.03)
        pause()
        sleep(0.05)
        if val1 == 1 and val2 == 1 and val3 == 1:
            T()
            return 0
        count += 1
    forwards()
    sleep(0.5)
    right()
    sleep(0.25)
    pause()
    sleep(0.1)
    count = 0
    while True:
        read()
        count += 1
        right()
        sleep(0.03)
        pause()
        sleep(0.05)
        if val1 == 1 or val2 == 1:
            break
        if count >= 300:
            break

def right_turn():
    global val1
    global val2
    global val3
    #If approaching from an angle, needs to check for T
    count = 0
    while count <= 3:
        read()
        forwards()
        sleep(0.03)
        pause()
        sleep(0.05)
        if val1 == 1 and val2 == 1 and val3 == 1:
            T()
            return 0
        count += 1
    forwards()
    sleep(0.5)
    left()
    sleep(0.25)
    pause()
    sleep(0.1)
    count = 0
    while True:
        read()
        count += 1
        left()
        sleep(0.03)
        pause()
        sleep(0.05)
        if val1 == 1 or val2 == 1:
            break
        if count >= 300:
            break
    
def T():
    print("Start")
    forwards()
    sleep(0.5)
    right()
    sleep(0.25)
    pause()
    sleep(0.1)
    count = 0
    global val1
    global val2
    global val3
    while True:
        read()
        count += 1
        right()
        sleep(0.03)
        pause()
        sleep(0.05)
        if val1 == 1 or val2 == 1:
            break
        if count >= 300:
            break
    forwards()
    global line_direction
    line_direction = "left"
    print("END")
    

line_direction = "left" # set to default as to which direction your robot USUALLY moves off of the line.
TIME_FROM_LEFT = None
TIME_FROM_RIGHT = None
while 1:
    read()
    if val2 == 1:
        if val1 == 0 and val3 == 0:
            forwards()
            sleep(0.07)
            pause()
            sleep(0.1)
        elif val1 == 1 and val2 == 1 and val3 == 1:
            T()
        elif val1 == 1 and val2 == 1 and val3 == 0: #Right turn
            #If approaching from an angle, needs to check for T
            right_turn()
            line_direction = "right"
        elif val1 == 0 and val2 == 1 and val3 == 1: # Left turn
            left_turn()
            line_direction = "left"
    elif val2 == 0 and val1 == 0 and val3 == 0:
        if line_direction == "left":
            left()
        else:
            right()
        sleep(0.01)
        pause()
        sleep(0.04)
    elif val2 == 0:
        if (val1 == 1 and val3 == 0): # Moved off straight line to the left (right sensor over line)
            if TIME_FROM_LEFT == None:
                count = 0
                while True:
                    read()
                    count += 1
                    left()
                    sleep(0.03)
                    pause()
                    sleep(0.05)
                    if val2 == 1:
                        break
                    if count >= 300:
                        break
                start = time()
                count = 0
                while True:
                    read()
                    count += 1
                    left()
                    sleep(0.03)
                    pause()
                    sleep(0.05)
                    if val2 == 0:
                        break
                    if count >= 300:
                        break
                end = time()
                TIME_FROM_LEFT = end - start - (count * 0.05)
            else:
                count = 0
                while True:
                    read()
                    count += 1
                    left()
                    sleep(0.03)
                    pause()
                    sleep(0.05)
                    if val2 == 1:
                        break
                    if count >= 300:
                        break
            left()
            sleep(TIME_FROM_LEFT)
        elif val1 == 0 and val3 == 1:
            if TIME_FROM_RIGHT == None:
                count = 0
                while True:
                    read()
                    count += 1
                    right()
                    sleep(0.03)
                    pause()
                    sleep(0.05)
                    if val2 == 1:
                        break
                    if count >= 300:
                        break
                start = time()
                count = 0
                while True:
                    read()
                    count += 1
                    right()
                    sleep(0.03)
                    pause()
                    sleep(0.05)
                    if val2 == 0:
                        break
                    if count >= 300:
                        break
                end = time()
                TIME_FROM_RIGHT = end - start - (count * 0.05)
            else:
                count = 0
                while True:
                    read()
                    count += 1
                    right()
                    sleep(0.03)
                    pause()
                    sleep(0.05)
                    if val2 == 1:
                        break
                    if count >= 300:
                        break
            right()
            sleep(TIME_FROM_RIGHT)



