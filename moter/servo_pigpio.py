#!/usr/bin/python
# -*- coding: utf-8 -*-

import pigpio
import time

SERVO_X = 26 # GPIO
START_V = 500 # us
END_V = 2400 # us

def get_pulsewidth(ang):
    ang += 90.0
    if ang < 0.0:
        ang = 0.0
    if ang > 180.0:
        ang = 180.0
    w = (END_V - START_V) * (float(ang) / 180.0) + START_V
    return w

pi1 = pigpio.pi()

try:
    for ang in [0, -90, 0, 90, 0, -90, -45, 0, 45, 90, 45, 0]:
        w = get_pulsewidth(ang)
        print "ang = %f , pulse width = %f" % (ang, w)
        pi1.set_servo_pulsewidth(SERVO_X, w)
        time.sleep(0.5)
        pi1.set_servo_pulsewidth(SERVO_X, 0)
        time.sleep(2.5)

except KeyboardInterrupt:
    pass

print "Done."
pi1.stop()
