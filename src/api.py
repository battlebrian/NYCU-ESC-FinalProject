from .car_controller import forward,backward,left,right,measure
from math import pi

import math
import blescan

def moveForward(length:float):
    forward(int(length*100/33*4096))

def moveBackward(length:float):
    backward(int(length*100/33*4096))

def getLocation(sock):
    locationList = []
    rssiDict = dict()   # create a dictionary(what can it do?
    returnedList = blescan.parse_events(sock)

    for beacon in returnedList:
        raw_uuid = ""
        for word in beacon.uuid.split('-'):
            raw_uuid = raw_uuid + word
        if raw_uuid == "00000000111111110000000000556601":
            if beacon.major=="12" and beacon.minor=="34":
                locationList.append(math.pow(10,((-56.829-int(beacon.rssi))/(10*1.190))))
            if beacon.major=="5566" and beacon.minor=="7788":
                locationList.append(math.pow(10,((-61.513-int(beacon.rssi))/(10*2.379))))
            if beacon.major=="1122" and beacon.minor=="3344":
                locationList.append(math.pow(10,((-36.092-int(beacon.rssi))/(10*4.579))))
    
    #return a list containing two distances 
    return locationList

def rotateCounterclockwise(degree:float):
    if degree > 0:
        left(int(degree/360*5888))
    elif degree < 0:
        right(int(-degree/360*5888))

def faceObstacle():
    dis = measure()

    return dis<1

def getServersDistance():
    return 10;
