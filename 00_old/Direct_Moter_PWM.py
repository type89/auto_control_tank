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

# 初期化
p0.start(0)
p1.start(0)

try:
        while True:
                for i in range(0,6):
                        new_duty = i*15
                        p0.ChangeDutyCycle(0)
                        p1.ChangeDutyCycle( new_duty )
                        print( new_duty )
                        time.sleep(1.0)
                for i in range(6,0,-1):
                        new_duty = i*15
                        p0.ChangeDutyCycle(0)
                        p1.ChangeDutyCycle( new_duty )
                        print( new_duty )
                        time.sleep(1.0)
                for i in range(0,6):
                        new_duty = i*15
                        p0.ChangeDutyCycle( new_duty )
                        p1.ChangeDutyCycle( 0 )
                        print( new_duty )
                        time.sleep(1.0)
                for i in range(6,0,-1):
                        new_duty = i*15
                        p0.ChangeDutyCycle( new_duty )
                        p1.ChangeDutyCycle( 0 )
                        print( new_duty )
                        time.sleep(1.0)

except KeyboardInterrupt:
        print("\nCtrl + c : Exit")
except:
        print("\nError : Exit")

p0.stop()
p1.stop()
GPIO.cleanup()


TRIG_PORT = 4
ECHO_PORT = 21
RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(TRIG_PORT, RPi.GPIO.OUT)
RPi.GPIO.setup(ECHO_PORT, RPi.GPIO.IN)

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

if __name__ == "__main__":
    try:
        i = 1
        while(i<100):
            L_Power(0.5)
            R_Power(0.5)
            cm = read_distance()
            print("distance=", cm)
            sleep(0.55555)
            if(cm < 5):
                i=9999

    except KeyboardInterrupt:
        pass
    RPi.GPIO.cleanup()
