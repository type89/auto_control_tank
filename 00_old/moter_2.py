#!/usr/bin/python
# coding: utf-8

import RPi.GPIO as GPIO
from time import time,sleep
import sys

# GPIO 14,15番を使用
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
p0 = GPIO.PWM(25, 50)
p1 = GPIO.PWM(24, 50)
p2 = GPIO.PWM(23, 50)
p3 = GPIO.PWM(22, 50)


TRIG_PORT = 4
ECHO_PORT = 21
GPIO.setup(TRIG_PORT, GPIO.OUT)
GPIO.setup(ECHO_PORT, GPIO.IN)

# HC-SR04で距離を測定する --- (*2)
def read_distance():
    # トリガーで信号を送出
    GPIO.output(TRIG_PORT, GPIO.LOW)
    sleep(0.001)
    # トリガーをHIGH→LOWに設定
    GPIO.output(TRIG_PORT, GPIO.HIGH)
    sleep(0.011)
    GPIO.output(TRIG_PORT, GPIO.LOW)

    # エコーに戻ってくる長さを調べる
    sig_start = sig_end = 0
    while GPIO.input(ECHO_PORT) == GPIO.LOW:
      sig_start = time()
      #print("sig_start = " + str(sig_start))
    while GPIO.input(ECHO_PORT) == GPIO.HIGH:
      sig_end = time()
      #print("sig_end = " + str(sig_end))

    # 経過時間が距離になっている --- (*3)
    duration = sig_end - sig_start
    distance = duration * 17000
    return distance


# 初期化
p0.start(0)
p1.start(0)
p2.start(0)
p3.start(0)

try:
    x=1
    while (x==1):
        cm = read_distance()
        print("distance=", cm)
        sleep(0.1)
        if(cm <= 0):
            cm =30
        if(cm < 10):
            x=0
        new_duty = 50
        p0.ChangeDutyCycle(0)
        p1.ChangeDutyCycle( new_duty )
        p2.ChangeDutyCycle(0)
        p3.ChangeDutyCycle( new_duty )
        sleep(0.05)
        #print( new_duty )

except KeyboardInterrupt:
        print("\nCtrl + c : Exit")
#except:
        #print("\nError : Exit")

p0.stop()
p1.stop()
p2.stop()
p3.stop()
GPIO.cleanup()
