from machine import Pin, PWM
from time import sleep, time

led = Pin(25, Pin.OUT)


# L C R
# 1 2 3 
sensor1 = Pin(18, Pin.IN)
sensor2 = Pin(19, Pin.IN)
sensor3 = Pin(20, Pin.IN)


IN2 = Pin(10, Pin.OUT)
IN1 = Pin(11, Pin.OUT)
IN3 = Pin(12, Pin.OUT)
IN4 = Pin(13, Pin.OUT)

ENA = PWM(Pin(0))
ENB = PWM(Pin(1))

ENA.freq(1000)
ENB.freq(1000)

#topspeed = 65025
    
ENA.duty_u16(65000)
ENB.duty_u16(55000)

def stop():
    IN1.low()
    IN2.low()
    IN3.low()
    IN4.low()
    
def forward():
    IN1.low()
    IN2.high()
    IN3.low()
    IN4.high()
    
def backward():
    IN1.high()
    IN2.low()
    IN3.high()
    IN4.low()
    
# just move one wheel to turn
def left1():
    IN1.low()
    IN2.high()

def right1():
    IN3.low()
    IN4.high()
    
# move the other wheel opposite to pivot
def left2():
    IN1.low()
    IN2.high()
    IN3.high()
    IN4.low()
    
def right2():
    IN1.high()
    IN2.low()
    IN3.low()
    IN4.high()
    

# centre the robot to O|O
def centre(prev):
    while 1:
        stop()
        sleep(0.05)
        l,c,r = sensor1.value(), sensor2.value(), sensor3.value()
        
        if c == 1:
            if prev == "l":
                prev = "r"
            else:
                prev = "l"
            return prev
        
        if l and not(c or r):
            prev = "r"
        elif r and not(c or l):
            prev = "l"
            
        if prev == "r":
            left1()
            sleep(0.05)
        else:
            right1()
            sleep(0.05)
            
    
def left_turn():
    forward()
    sleep(0.5)
    stop()
    sleep(0.02)
    left2()
    sleep(0.5)
    
    while 1:
        stop()
        sleep(0.05)
        l,c,r = sensor1.value(), sensor2.value(), sensor3.value()
        
        if c:
            return "l"
        
        left1()
        sleep(0.04)
    
    
def right_turn():
    forward()
    sleep(0.5)
    stop()
    sleep(0.02)
    right2()
    sleep(0.5)
    
    while 1:
        stop()
        sleep(0.05)
        l,c,r = sensor1.value(), sensor2.value(), sensor3.value()
        
        if c:
            return "r"
        
        right1()
        sleep(0.04)
        
        
prev = "r"    
start = time()

while 1:
    stop()
    sleep(0.05)
    
    l,c,r = sensor1.value(), sensor2.value(), sensor3.value()
    
    
    # O|O
    if c and not(l or r):
        forward()
        sleep(0.05)
        
    # OOO
    elif not(l or c or r):
        prev = centre(prev)
        
    # |OO      
    elif l and not(c or r):
        prev = centre("r")
        
    # OO|      
    elif r and not(c or l):
        prev = centre("l")
        
    # |O|
    elif l and r and not c:
        end = time()
        print(end-start)
        break
    
    else:
        l1,c1,r1 = sensor1.value(), sensor2.value(), sensor3.value()
        forward()
        sleep(0.2)
        stop()
        sleep(0.05)
        
        l2,c2,r2 = sensor1.value(), sensor2.value(), sensor3.value()
        backward()
        sleep(0.2)
        stop()
        sleep(0.02)
        
        # XXX
        # ||X
        if l1 and c1:
            prev = left_turn()
            
        # X|X
        # O|X
        elif c2:
            forward()
            sleep(0.1)
            stop()
        
        # XOX
        # O||
        else:
            prev = right_turn()
            
