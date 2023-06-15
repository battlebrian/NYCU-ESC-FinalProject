from .car_controller import forward,backward,left,right,measure
from math import pi



def moveForward(length:float):
    forward(int(length*100/33*4096))

def moveBackward(length:float):
    backward(int(length*100/33*4096))

def getLocation():
    pass
    #return a list containing two distances 

def rotateCounterclockwise(degree:float):
    if degree > 0:
        left(int(degree/360*5888))
    elif degree < 0:
        right(int(-degree/360*5888))

def faceObstacle():
    dis = measure()

    return dis<1

def getServersDistance():
    pass