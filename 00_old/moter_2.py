#!/usr/bin/python
# coding: utf-8

import RPi.GPIO as GPIO
import time
import sys

# GPIO 14,15番を使用
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
p0 = GPIO.PWM(25, 50)
p1 = GPIO.PWM(24, 50)

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
      print("sig_start = " + str(sig_start))
    while GPIO.input(ECHO_PORT) == GPIO.HIGH:
      sig_end = time()
      print("sig_end = " + str(sig_end))

    # 経過時間が距離になっている --- (*3)
    duration = sig_end - sig_start
    distance = duration * 17000
    return distance


# 初期化
p0.start(0)
p1.start(0)

try:
    while True:
        new_duty = 15
        p0.ChangeDutyCycle(0)
        p1.ChangeDutyCycle( new_duty )
        print( new_duty )
        cm = read_distance()
        print("distance=", cm)

except KeyboardInterrupt:
        print("\nCtrl + c : Exit")
except:
        print("\nError : Exit")

p0.stop()
p1.stop()
GPIO.cleanup()
