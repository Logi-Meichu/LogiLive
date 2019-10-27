import RPi.GPIO as GPIO
import time

CONTROL_PIN = 22
PWM_FREQ = 50
STEP = 15
#GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(CONTROL_PIN, GPIO.OUT)

pwm = GPIO.PWM(CONTROL_PIN, PWM_FREQ)
pwm.start(2.5)

try:
  while True:
    for i in range(10):
      pwm.ChangeDutyCycle(float(5 + (4.5/10)*i))
      time.sleep(0.3)
    for i in range(10):
      pwm.ChangeDutyCycle(float(9.5 - (4.5/10)*i))
      time.sleep(0.3)
    time.sleep(3)
    
except KeyboardInterrupt:
	print('interrupt')
finally:
   pwm.stop()
   GPIO.cleanup()
