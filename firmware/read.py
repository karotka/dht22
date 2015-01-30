#!/usr/bin/env python

import serial

SERIAL = "/dev/tty.usbserial-A90ZBP5L"

ser = serial.Serial(SERIAL, 1200, stopbits=2)

def readData():
    buff = []
    while 1:
        v = ser.read()
        if ord(v) == 10:
            print "". join(buff)
            return
        else:
            buff.append(v)

while 1:
    readData()
