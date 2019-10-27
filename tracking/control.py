import RPi.GPIO as GPIO
import time
from conn import ConnClient  
from common import setup_logger

CONTROL_PINX = 22
CONTROL_PINY = 17

PWM_FREQ = 50
STEP = 15

xMax = 640
yMax = 480
xTh1 = 250
yTh1 = 120
xTh2 = 300
yTh2 = 360
#global curDutyX
#global curDutyY

curDutyX = 7.5
curDutyY = 7.5

# GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(CONTROL_PINX, GPIO.OUT)
GPIO.setup(CONTROL_PINY, GPIO.OUT)

pwmX = GPIO.PWM(CONTROL_PINX, PWM_FREQ)
pwmY = GPIO.PWM(CONTROL_PINY, PWM_FREQ)
pwmX.start(7.5)
pwmY.start(7.5)

# def angle_to_duty_cycle(angle=0):
#     duty_cycle = (0.05 * PWM_FREQ) + (0.19 * PWM_FREQ * angle / 180) + 5
#     return duty_cycle


#for x
def turnX(x):
  global curDutyX
  cur_speed = 1.08889
  if x > xTh2 and curDutyX < 10.9:
      pwmX.ChangeDutyCycle(curDutyX - cur_speed)
      time.sleep(0.5)
      curDutyX -= cur_speed
      pwmX.ChangeDutyCycle(0)
      print('curDuty: {}'.format(curDutyY))
  elif x < xTh1 and curDutyX > 4.1:
      pwmX.ChangeDutyCycle(curDutyX + cur_speed)
      time.sleep(0.5)
      curDutyX += cur_speed
      pwmX.ChangeDutyCycle(0)
      print('curDutyX: {}'.format(curDutyX))
  return None
     
def OutOfFrameX(x=-1):
 if x < 0:
      return 0
 if x < xTh1 or x > xTh2:
      return 1
 return 0

#for y
def turnY(y):
  global curDutyY
  if y > yTh2 and curDutyY < 10.9:
      pwmY.ChangeDutyCycle(curDutyY + 1.58889)
      time.sleep(0.5)
      curDutyY += 1.58889
      pwmY.ChangeDutyCycle(0)
  elif y < yTh1 and curDutyY > 4.1:
      pwmY.ChangeDutyCycle(curDutyY - 1.58889)
      time.sleep(0.5)
      curDutyY -= 1.58889
      pwmY.ChangeDutyCycle(0)
  return None
     
def OutOfFrameY(y=-1):
 if y < 0:
      return 0
 if y < yTh1 or y > yTh2:
      return 1
 return 0


def control(xin, yin):
  print('control({}, {})'.format(xin, yin))
  #logger.info('control({}, {})'.format(xin, yin))
  x = xin
  y = yin
  if OutOfFrameX(x) and OutOfFrameY(y):
    turnX(x)
    turnY(y)
  elif OutOfFrameY(y):
    turnY(y)
  elif OutOfFrameX(x):
    turnX(x)
    
#main

import numpy as np
def test():
  for i in range(50):
    x = np.random.randint(10, 600)
    y = np.random.randint(10, 450)
    control(x, y)
    time.sleep(np.random.randint(0, 3))

if __name__ == '__main__':
  logger = setup_logger()
  conn = ConnClient(host='172.20.10.7', port=8202, logger=logger)
  
  while True:
    data = conn.read()
    print('receive x = {}, y = {}'.format(data['x'], data['y']))
    control(data['x'], data['y'])



