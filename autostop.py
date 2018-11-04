import webiopi
from time import sleep, time
import RPi.GPIO

webiopi.setDebug()

GPIO = webiopi.GPIO
#GPIO = RPi.GPIO

class DCMotor:
	_pin1 = 0
	_pin2 = 0

	def __init__(self, pin1, pin2):
		self._pin1 = pin1
		self._pin2 = pin2
		GPIO.setFunction( self._pin1, GPIO.PWM )
		GPIO.setFunction( self._pin2, GPIO.PWM )

	def __del__(self):
		self.write(0.0) # stop

	def write(self, ratio):
		if 1.0 < ratio:	# saturation
			ratio = 1.0
		if -1.0 > ratio:	# saturation
			ratio = -1.0
		if 0.01 > ratio and -0.01 < ratio:	# stop
			GPIO.pwmWrite(self._pin1, 0.0)
			GPIO.pwmWrite(self._pin2, 0.0)
		elif 0 < ratio:	# Normal rotation
			GPIO.pwmWrite(self._pin1, ratio)
			GPIO.pwmWrite(self._pin2, 0.0)
		else:	# Reverse rotation
			GPIO.pwmWrite(self._pin1, 0.0)
			GPIO.pwmWrite(self._pin2, -ratio)

#g_motorL = DCMotor( 5, 6 )		# Left motor
g_motorL = DCMotor( 25, 24 )		# Left motor
#g_motorR = DCMotor( 13, 19 )	# Right motor
g_motorR = DCMotor( 23, 22 )	# Right motor

@webiopi.macro
def L_Power(LM):
	LM = float(LM)
	g_motorL.write(LM)

@webiopi.macro
def R_Power(RM):
	RM = float(RM)
	g_motorR.write(RM)

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
      #print("sig_start = " + str(sig_start))
    while RPi.GPIO.input(ECHO_PORT) == RPi.GPIO.HIGH:
      sig_end = time()
      #print("sig_end = " + str(sig_end))

    # 経過時間が距離になっている --- (*3)
    duration = sig_end - sig_start
    distance = duration * 17000
    return distance

PNO=17
RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(PNO, RPi.GPIO.OUT)


if __name__ == "__main__":
    try:
        i = 1
        while(i<100):
            RPi.GPIO.output(PNO, RPi.GPIO.LOW)
            cm = read_distance()
            print("distance=", cm)
            sleep(0.1)
            if(cm <= 0):
                cm = 50
            if(cm < 25):
                #i=9999
                RPi.GPIO.output(PNO, RPi.GPIO.HIGH)
                L_Power(-0.5)
                R_Power(-0.5)
                sleep(1)
                L_Power(0.5)
                R_Power(-0.5)
                sleep(1.2)
            sleep(0.01)
            L_Power(0.53)
            R_Power(0.49)

    except KeyboardInterrupt:
        pass
    RPi.GPIO.cleanup()
