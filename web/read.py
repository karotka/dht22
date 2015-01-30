#!/usr/bin/env python

import serial
import sqlite3
import datetime

SERIAL = "/dev/tty.usbserial-A90ZBP5L"

ser = serial.Serial(SERIAL, 1200, stopbits=2)

def getConnection():
    return sqlite3.connect("data.db")

def readData():
    buff = []
    data = dict()
    while 1:
        v = ser.read()
        if ord(v) == 10:
            d = "". join(buff)
            h, t = d.split("\t")
            data["hum"] = h.split(":")[1]
            data["temp"] = t.split(":")[1] 
            return data
        else:
            buff.append(v)

buff = dict()
oldMin = ""
while 1:
    d = datetime.datetime.now() 
    data = readData()
    minute = "%02d-%02d-%02d %02d:%02d" % (d.year, d.month, d.day, d.hour, d.minute)

    if buff.has_key(minute):  
        buff[minute].append(data)
        oldMin = minute
    else:
        buff[minute] = list()
        it = buff.get(oldMin, None)
        if it:
            aT = list()
            aH = list()
            for i in it:
                aT.append(float(i["temp"]))
                aH.append(float(i["hum"]))
            conn = getConnection()
            c = conn.cursor()
            c.execute("INSERT INTO data (date, temp, hum) VALUES (DATETIME('now'), ?, ?)",
                (sum(aT) / len(aT), sum(aH) / len(aH)))
            conn.commit()
        if oldMin:
            try:
                del buff[oldMin]
            except:
                pass
    
