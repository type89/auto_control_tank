from time import sleep, time
import RPi.GPIO as GPIO

PNO = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(PNO, GPIO.OUT)


# HC-SR04 GPIOポートの設定 --- (*1)
TRIG_PORT = 4
ECHO_PORT = 21
GPIO.setmode(GPIO.BCM)
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
    while GPIO.input(ECHO_PORT) == GPIO.HIGH:
      sig_end = time()
    
    # 経過時間が距離になっている --- (*3)
    duration = sig_end - sig_start
    distance = duration * 17000
    return distance

if __name__ == '__main__':
    try:
        while True:
            cm = read_distance()
            print("distance=", cm)
            sleep(0.3)
            if(cm < 10):
                GPIO.output(PNO, GPIO.HIGH)
            else:
                GPIO.output(PNO, GPIO.LOW)

    except KeyboardInterrupt:
        pass
    GPIO.cleanup()


