import cv2
import numpy as np
import time
import RPi.GPIO as GPIO

'''GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.output(7, False)
GPIO.output(11, True)
GPIO.output(13, False)
GPIO.output(15, True)'''

cap = cv2.VideoCapture(0)
def traffic():
	_, frame = cap.read()
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	lower_red = np.array([140, 100, 100])
	upper_red = np.array([189, 255, 255])
	mask = cv2.inRange(hsv, lower_red, upper_red)
	res = cv2.bitwise_and(frame, frame, mask = mask)
	grey = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
	value = (35, 35)
	blurred = cv2.GaussianBlur(grey, value, 0)
	_, thresh1 = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
	cv2.imshow('grey', thresh1)
	image, contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	cnt1 = min(contours, key = lambda x: cv2.contourArea(x))
	x, y, w, h = cv2.boundingRect(cnt1)
	cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 0)
	area = cv2.contourArea(cnt1, True)
	cv2.drawContours(frame, contours, -1, (0, 255, 0), 10)
	print(area)
	'''if area > 100:
		GPIO.output(7, False)
		GPIO.output(11, False)
		GPIO.output(13, False)
		GPIO.output(15, False)
		time.sleep(2)'''
	_, t2 = cv2.threshold(res,127,255, 0)
	cv2.imshow('threshold', t2)
	cv2.imshow('frame', frame)
	cv2.imshow('mask', mask)
	cv2.imshow('res', res)
	'''GPIO.output(7, False)
	GPIO.output(11, True)
	GPIO.output(13, False)
	GPIO.output(15, True)'''
	return area
k = 0
while k < 50:
	traffic()
	k = k + 1
cv2.destroyAllWindows()
cap.release()
