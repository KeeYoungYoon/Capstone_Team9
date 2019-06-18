import cv2
import numpy as np
#import RPi.GPIO as GPIO
from time import sleep
#cap = cv2.VideoCapture(0)
b=-1
cap=cv2.VideoCapture('t1.mp4')
prev_state=0
i=0
def findNonZero(rgb_image):
  rows, cols, _ = rgb_image.shape
  counter = 0
  for row in range(rows):
    for col in range(cols):
      pixel = rgb_image[row, col]
      if sum(pixel) != 0:
        counter = counter + 1
  return counter

def red_green(rgb_image):
    global prev_state
    hsv = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2HSV)
    sum_saturation = np.sum(hsv[:,:,1])
    area = 48*48
    avg_saturation = sum_saturation / area

    sat_low = int(avg_saturation * 1.1)
    val_low = 140

# Green
    lower_green = np.array([55,50,50])
    upper_green = np.array([65,255,255])
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    green_result = cv2.bitwise_and(rgb_image, rgb_image, mask = green_mask)
    cv2.imshow('re',green_result)

# Red
    lower_red = np.array([112,sat_low,val_low])
    upper_red = np.array([140,255,255])
    red_mask = cv2.inRange(hsv, lower_red, upper_red)
    red_result = cv2.bitwise_and(rgb_image, rgb_image, mask = red_mask)
    #cv2.imshow('re',red_result)
    sum_green = findNonZero(green_result)
    #print(sum_green)
    sum_red = findNonZero(red_result)
    #print(sum_red)
    #cv2.imshow('asdf',red_mask)
    #if sum_red<=1 and prev_state==0:
    #    prev_state=1
    #    return 1
    #if sum_red>2:
    #    prev_state=0
    #    return 0
    #        print('red')
    #if sum_green>sum_red+30:
    #    return 'red'
    if sum_red>sum_green:
        prev_state=0
        return 1
    else:
        prev_state=1
        return 0
    #if sum_red != 0:
    #    return 'red' # Red
    #else:
    #return 'green' # Green
    #ret, frame = cap.read()
#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BCM)
#buzzer=23
#GPIO.setup(buzzer,GPIO.OUT)

while True:
          ret,frame=cap.read()
          crop = frame[250:280,300:400]
          st_img = cv2.resize(crop, (48,48))
          b-=1
          if i==0:
              i=i+1
              continue
          #print(i)
          #st_img=cv2.resize(crop,(96,96))
          #print(i)
          #if(red_green(st_img)==1):
          if(red_green(st_img)>0):
              print('red')
          else:
              print('green')
        #      if(prev_state==0):
        #          GPIO.output(buzzer,GPIO.LOW)
        #      print('beep')
        #      b=3
        # if(b==0):
        #      GPIO.output(buzzer,GPIO.HIGH)

        #  cv2.imshow('img',frame)
          cv2.imshow('crop',crop)
          #cv2.imshow('st',st_img)
         # cv2.imwrite('l.jpg',frame)
         # cv2.imwrite('j.jpg',crop)
          #cv2.imshow('im',in_img)
          #if(input('q')):
          if cv2.waitKey(1) & 0xFF == ord('q'):
                  break
    #in_img=cv2.imread('1.PNG', cv2.IMREAD_COLOR)


cv2.waitKey(0)
cv2.destroyAllWindows()
cap.release()
