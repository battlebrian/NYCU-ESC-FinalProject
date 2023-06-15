#!/usr/bin/python3
import RPi.GPIO as GPIO
import keyboard
import time

v = 343
TRIGGER_PIN = 16
ECHO_PIN = 26
GPIO.setmode( GPIO.BCM )
GPIO.setup(TRIGGER_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

def measure():
    GPIO.output(TRIGGER_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIGGER_PIN, GPIO.LOW)
    pulse_start = time.time()
    while GPIO.input(ECHO_PIN) == GPIO.LOW:
        pulse_start = time.time()
    while GPIO.input(ECHO_PIN) == GPIO.HIGH:
        pulse_end = time.time()
    t = pulse_end - pulse_start
    d = t * v
    d = d/2
    return d*100
    

# 11 13 15 16 18 22 29 31
in1 = 17
in2 = 27
in3 = 22
in4 = 23
in5 = 24
in6 = 25
in7 = 5
in8 = 6
 
# careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move
step_sleep = 0.002
 
step_count = 4096 # 5.625*(1/64) per step, 4096 steps is 360°
 
direction = False # True for clockwise, False for counter-clockwise
 
# defining stepper motor sequence (found in documentation http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
step_sequence_r = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]
step_sequence_l = [[0,0,0,1],
                 [0,0,1,1],
                 [0,0,1,0],
                 [0,1,1,0],
                 [0,1,0,0],
                 [1,1,0,0],
                 [1,0,0,0],
                 [1,0,0,1]]
 
# setting up
GPIO.setup( in1, GPIO.OUT )
GPIO.setup( in2, GPIO.OUT )
GPIO.setup( in3, GPIO.OUT )
GPIO.setup( in4, GPIO.OUT )
GPIO.setup( in5, GPIO.OUT )
GPIO.setup( in6, GPIO.OUT )
GPIO.setup( in7, GPIO.OUT )
GPIO.setup( in8, GPIO.OUT )
 
# initializing
GPIO.output( in1, GPIO.LOW )
GPIO.output( in2, GPIO.LOW )
GPIO.output( in3, GPIO.LOW )
GPIO.output( in4, GPIO.LOW )
GPIO.output( in5, GPIO.LOW )
GPIO.output( in6, GPIO.LOW )
GPIO.output( in7, GPIO.LOW )
GPIO.output( in8, GPIO.LOW )
 
 
motor_pins_l = [in1,in2,in3,in4]
motor_pins_r = [in5,in6,in7,in8]
motor_step_counter_l = 0
motor_step_counter_r = 0
 
 
def cleanup():
    GPIO.output( in1, GPIO.LOW )
    GPIO.output( in2, GPIO.LOW )
    GPIO.output( in3, GPIO.LOW )
    GPIO.output( in4, GPIO.LOW )
    GPIO.output( in5, GPIO.LOW )
    GPIO.output( in6, GPIO.LOW )
    GPIO.output( in7, GPIO.LOW )
    GPIO.output( in8, GPIO.LOW )
    GPIO.cleanup()
 
def forward(n):
    global motor_step_counter_l, motor_step_counter_r
    for i in range(n):
        for lpin in range(0, len(motor_pins_l)):
            GPIO.output( motor_pins_l[lpin], step_sequence_l[motor_step_counter_l][lpin] )
        for rpin in range(0, len(motor_pins_r)):
            GPIO.output( motor_pins_r[rpin], step_sequence_r[motor_step_counter_r][rpin] )
        motor_step_counter_l = (motor_step_counter_l + 2) % 8
        motor_step_counter_r = (motor_step_counter_r + 2) % 8
        time.sleep( step_sleep )

def backward(n):
    global motor_step_counter_l, motor_step_counter_r
    for i in range(n):
        for lpin in range(0, len(motor_pins_l)):
            GPIO.output( motor_pins_l[lpin], step_sequence_l[motor_step_counter_l][lpin] )
        for rpin in range(0, len(motor_pins_r)):
            GPIO.output( motor_pins_r[rpin], step_sequence_r[motor_step_counter_r][rpin] )
        motor_step_counter_l = (motor_step_counter_l - 2) % 8
        motor_step_counter_r = (motor_step_counter_r - 2) % 8
        time.sleep( step_sleep )

def right(n):
    global motor_step_counter_l, motor_step_counter_r
    for i in range(n):
        for lpin in range(0, len(motor_pins_l)):
            GPIO.output( motor_pins_l[lpin], step_sequence_l[motor_step_counter_l][lpin] )
        for rpin in range(0, len(motor_pins_r)):
            GPIO.output( motor_pins_r[rpin], step_sequence_r[motor_step_counter_r][rpin] )
        motor_step_counter_l = (motor_step_counter_l - 2) % 8
        motor_step_counter_r = (motor_step_counter_r + 2) % 8
        time.sleep( step_sleep )

def left(n):
    global motor_step_counter_l, motor_step_counter_r
    for i in range(n):
        for lpin in range(0, len(motor_pins_l)):
            GPIO.output( motor_pins_l[lpin], step_sequence_l[motor_step_counter_l][lpin] )
        for rpin in range(0, len(motor_pins_r)):
            GPIO.output( motor_pins_r[rpin], step_sequence_r[motor_step_counter_r][rpin] )
        motor_step_counter_l = (motor_step_counter_l + 2) % 8
        motor_step_counter_r = (motor_step_counter_r - 2) % 8
        time.sleep( step_sleep )
try:
    while True:
        print("wired")
        print("dis: ", measure())
        if measure() < 15:
            backward(512)
        if measure() < 30:
            right(512)
        forward(256)
 
except KeyboardInterrupt:
    cleanup()
    exit( 1 )
 
cleanup()
exit( 0 )