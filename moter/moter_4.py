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

#LED
LED = 17
GPIO.setup(LED, GPIO.OUT)

#GPIO26をサーボの制御パルスの出力に設定
gp_out = 26
GPIO.setup(gp_out, GPIO.OUT)

#HC-SR04
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
servo = GPIO.PWM(gp_out, 50)
servo.start(0)

def stop():
    p0.ChangeDutyCycle(0)
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(0)
    p3.ChangeDutyCycle(0)
    return

def forward():
    p0.ChangeDutyCycle(60)
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(69)
    p3.ChangeDutyCycle(0)
    return

def back(keeptime):
    p0.ChangeDutyCycle(0)
    p1.ChangeDutyCycle(56)
    p2.ChangeDutyCycle(0)
    p3.ChangeDutyCycle(50)
    sleep(keeptime)
    return

def turn_right(keeptime):
    p0.ChangeDutyCycle(56)
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(0)
    p3.ChangeDutyCycle(50)
    sleep(keeptime)
    return

def turn_left(keeptime):
    p0.ChangeDutyCycle(0)
    p1.ChangeDutyCycle(56)
    p2.ChangeDutyCycle(50)
    p3.ChangeDutyCycle(0)
    sleep(keeptime)
    return

def led(led_flag):
    if(led_flag ==1):
        GPIO.output(LED, GPIO.HIGH)
    else:
        GPIO.output(LED, GPIO.LOW)
    return

def kubihuri():
    servo.ChangeDutyCycle(2.5)
    sleep(0.5)
    servo.ChangeDutyCycle(7.25)
    sleep(0.5)
    servo.ChangeDutyCycle(12)
    sleep(0.5)
    servo.ChangeDutyCycle(7.25)
    sleep(0.5)
    return


try:
    x=1
    while (x==1):
        cm = read_distance()
        print("distance=", cm)
        sleep(0.15)
        if(cm <= 0):
            cm =100
        if(cm < 12):
            stop()
            led(1)
            back(2.0)
           # turn_right(1.3)
            led(0)
        if(cm < 30):
            led(1)
            stop()
            back(1.0)
            turn_right(0.8)
            right_cm = read_distance()
            turn_left(1.6)
            left_cm = read_distance()
            if(right_cm > left_cm):
                turn_right(1.6)
            led(0)
        forward()
        sleep(0.1)
        #print( new_duty )

except KeyboardInterrupt:
        print("\nCtrl + c : Exit")
#except:
        #print("\nError : Exit")

stop()
servo.stop()
GPIO.cleanup()
