#!/usr/bin/python
# coding: utf-8

import RPi.GPIO as GPIO
import time
import sys

TRIG_PORT = 4
ECHO_PORT = 21
RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(TRIG_PORT, RPi.GPIO.OUT)
RPi.GPIO.setup(ECHO_PORT, RPi.GPIO.IN)

# GPIO 14,15番を使用
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
p0 = GPIO.PWM(25, 50)
p1 = GPIO.PWM(24, 50)


# HC-SR04で距離を測定する --- (*2)
def read_distance():
    # トリガーで信号を送出
    RPi.GPIO.output(TRIG_PORT, RPi.GPIO.LOW)
    sleep(0.001)
    # トリガーをHIGH→LOWに設定
    RPi.GPIO.output(TRIG_PORT, RPi.GPIO.HIGH)
    sleep(0.011)
    RPi.GPIO.output(TRIG_PORT, RPi.GPIO.LOW)

    # エコーに戻ってくる長さを調べる
    sig_start = sig_end = 0
    while RPi.GPIO.input(ECHO_PORT) == RPi.GPIO.LOW:
      sig_start = time()
      print("sig_start = " + str(sig_start))
    while RPi.GPIO.input(ECHO_PORT) == RPi.GPIO.HIGH:
      sig_end = time()
      print("sig_end = " + str(sig_end))

    # 経過時間が距離になっている --- (*3)
    duration = sig_end - sig_start
    distance = duration * 17000
    return distance


# 初期化
p0.start(0)
p1.start(0)


if __name__ == "__main__":
    try:
        x=1
        while (x=1):
            new_duty = 30
            p0.ChangeDutyCycle(0)
            p1.ChangeDutyCycle( new_duty )
            cm = read_distance()
            print("distance=", cm)
            sleep(0.55555)
            if(cm < 5):
                i=9999

except KeyboardInterrupt:
        print("\nCtrl + c : Exit")
except:
        print("\nError : Exit")

p0.stop()
p1.stop()
GPIO.cleanup()
