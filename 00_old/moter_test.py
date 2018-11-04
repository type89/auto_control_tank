import webiopi

webiopi.setDebug()

GPIO = webiopi.GPIO

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

if __name__ == "__main__":
    i = 1
    while(i<100):
        L_Power(0.5)
        R_Power(0.5)
        print(i)
        #i = i+1
