#!/usr/bin/env python
# _*_ coding:utf_8  _*_
import cv2
import numpy as np
#import mahotas
from matplotlib import pyplot as plt
import os
import math
import time
import picamera
import RPi.GPIO as GPIO
import socket
import sys
from PIL import Image
import requests
import pytesseract
from StringIO import StringIO
from pytesseract import image_to_string  
from RPIO import PWM
from select import *
import sys
from time import ctime
from threading import *
import thread, time
from threading import Thread
import threading

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT) #11   Red
GPIO.output(17,False)
GPIO.setup(18,GPIO.OUT) #12   Green
GPIO.output(18,False)
GPIO.setup(27,GPIO.IN)  #13   rain sensor 

GPIO.setup(22,GPIO.OUT) #15   STOP
GPIO.output(22,False)
GPIO.setup(23,GPIO.OUT) #16   GO
GPIO.output(23,False)
GPIO.setup(24,GPIO.OUT) #18   Servo M
GPIO.output(24,False)
GPIO.setup(25,GPIO.OUT) #22   rain check
GPIO.output(25,False)
GPIO.setup(12,GPIO.OUT) #32   rain out
GPIO.output(12,False)
GPIO.setup(16,GPIO.IN)  #36   battery3

GPIO.setup(20,GPIO.IN)  #38   battery2

GPIO.setup(21,GPIO.IN)  #40   battery1


#11pin red 			#12pin green
#13pin Rain(in) 		#14pin GND
#15pin STOP -> OCR (pi -> FPGA) #16pin START,GO -> OCR (pi -> FPGA)
			        #18pin servo motor
				#22pin rain check
				#32pin rain out (pi -> FPGA)
				#36pin battery3 (FPGA -> pi)
				#38pin battery2 (FPGA -> pi)
				#40pin battery1 (FPGA -> pi)
				

rain=27
servo=24
Sval=1
Sint=0.1
data=""

HOST = "192.168.0.28"
PORT = 5555



Servo=PWM.Servo()
camera=picamera.PiCamera()
#start test
GPIO.output(25,True)
time.sleep(1)
GPIO.output(25,False)
time.sleep(1)
GPIO.output(25,True)
time.sleep(1)
GPIO.output(25,False)
time.sleep(1) 
	
#server->client
def do_some_stuffs_with_input(input_string):
	if input_string == "start":
		print("[server]start")
		input_string = "START ! \n"
		GPIO.output(23,True)	
	elif input_string == "stop":
		print("[server]stop")
		input_string = "STOP ! \n"
		GPIO.output(17,True)
	elif input_string == "rain":
		input_string = "Raining ! \n"
	elif input_string == "red":
		input_string = "RED ! \n"
	elif input_string == "green":
		input_string = "GREEN ! \n"
	elif input_string == "clean":
		input_string = "CLEAN ! \n"
	elif input_string == "battery":
		input_string = battery_check(input_string)
	else :
		input_string = input_string + " An invalid command . \n"
	return input_string


#p3 p2 p1
#1  0   0      0%
#0  1   0     25%
#1  1   0     50%
#0  0   1     75%
#1  0   1    100%
def battery_check(input_string):  
	print("[server]battery check")
# input_string="100%\n"

	b1=GPIO.input(16)
	b2=GPIO.input(20)
	b3=GPIO.input(21)
	if b1== 1:
		if b2== 1:
			if b2== 0:
				input_string="50%\n"
				
		else:
			if b3== 1:
				input_string="100%\n"
			else:
				input_string="0%\n"
	else:
		if b2== 1:
			if b3== 0:
				input_string="25%\n"
		else:
			if b3== 1:
				input_string="75%\n" 
	return input_string


def server_work():
	try:
		temp=1
		while True: 		
			print("Do Server's work!")
        # TODO
	#image = cv2.imread("light_r.png")
			camera.caputre('capture.jpg',resize=(640,640))
			image2 =cv2.imread("capture.jpg")
			rows,cols =image2.shape[:2]	
	
			M1=cv2.getRotationMatrix2D((cols/2,rows/2),180,1)
			image=cv2.warpAffine(image2,M1,(cols,rows))
		
			GPIO.output(17,False) 
			GPIO.output(18,False)
			GPIO.output(22,False)
			GPIO.output(23,False)

			element=cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
			hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)   #convert BGR to MSV
	       
			speed = image	
		#	cv2.imwrite('speed_file.png',speed)
	
	
 #define color strenght parameters in msv   
 #G 70 100 100/90 255 255    //// 50 80 80/70 255 255 
 #Y 20 100 100/40 255 255
 #R 170 100 100/190 255 255
 #site=www.rapidtables.com ->Web Design ->web color ->RGB 
	
			rweaker = np.array([165,50,80]) #red sign 90 80
			rstronger = np.array([185, 255, 255])
			pweaker = np.array([120, 70, 60]) #purple letter
			pstronger = np.array([140, 255,255])
			gweaker = np.array([30, 80, 70])  #yellow_green sign 170 250 50
			gstronger = np.array([50, 255,255])

		#yweaker = np.array([15, 70, 60])
                #ystronger = np.array([40, 255,255])
		#gweaker = np.array([50, 50, 0]) #50 0 80 80			
		#gstronger = np.array([70, 255,255]) 
	

#threshold the MSV image to obtain input color
	
	
			rain_value=GPIO.input(rain)
			if rain_value== 0:
		
               					
				GPIO.output(25,True) #LED
				#GPIO.output(12,True) #(pi -> FPGA)

				if temp==1:
					
					Servo.set_servo(servo,1000)
					time.sleep(0.5)
				else:
					Servo.set_servo(servo,2200)
					time.sleep(0.5)
				temp *= -1
				Servo.stop_servo(servo)
			else:
			       	       
				GPIO.output(25,False) #LED
				#GPIO.output(12,False) #(pi -> FPGA)
				
	
		        #print "start"
	
			check=0;
		#red
			mask = cv2.inRange(hsv,rweaker,rstronger)
			eroded = cv2.erode(mask,element)
			traffic = cv2.dilate(eroded,element)
			intRows,intColumns = traffic.shape
			circles = cv2.HoughCircles(traffic,cv2.HOUGH_GRADIENT,1,50,param1=50,param2=11,minRadius=7,maxRadius=25)
	
			if circles is not None:
				for circle in circles[0,:]:
					x,y,r=circle
					print("red ball position x= "+str(x)+",y= "+str(y)+",r="+str(r))
					cv2.circle(image,(x,y),r,(255,255,0),1)
					GPIO.output(17,True)
					#GPIO.output(22,True) #(pi -> FPGA)
					check=check-1
				
      				
				

			else:
				check=check+1
			
		
		#green
			mask = cv2.inRange(hsv,gweaker,gstronger)
			eroded = cv2.erode(mask,element)
			traffic = cv2.dilate(eroded,element)
			intRows,intColumns = traffic.shape
			circles = cv2.HoughCircles(traffic,cv2.HOUGH_GRADIENT,1,50,param1=50,param2=11,minRadius=7,maxRadius=25)
	
			if circles is not None:
				for circle in circles[0,:]:
					x,y,r=circle
					print("green ball position x= "+str(x)+",y= "+str(y)+",r="+str(r))
					cv2.circle(image,(x,y),r,(255,255,0),1)

					GPIO.output(18,True)
					#GPIO.output(23,True) #(pi -> FPGA)

				#       GPIO.output(18,False)
				#       GPIO.output(23,False) #(pi -> FPGA)

					check=check-1
	
            
				
			else:
				check=check+1	
	
		
			if check==2:
				print("Not Found!")	
		#check 0==red 1==green 2==NONE
	      	
			hsv2 = cv2.cvtColor(speed, cv2.COLOR_BGR2HSV)
			mask2 = cv2.inRange(hsv2,pweaker,pstronger)
		
			eroded2 = cv2.erode(mask2,element)
			sign = cv2.dilate(eroded2,element)
			sign = ~sign
			intRows,intColumns = sign.shape	
			cv2.imwrite('speed_ocr_file.png',sign)

		#detect color and draw  
		#ret,thresh = cv2.threshold(temp,127,255,0)
		#_, cnts,_ = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		#c= max(cnts,key=cv2.contourArea)
		#peri = cv2.arcLength(c,True)
		#approx = cv2.approxPolyDP(c,0.01 * peri,True)
		#cv2.drawContours(image,[approx],-1,(0,0,255),2)
	
		#image show
	#		cv2.imshow('Image',image)
	#		cv2.imshow('Result',traffic)
	#		cv2.imshow('speed',speed)
	#		cv2.imshow('sign_ocr',sign)
	#		mahotas.imsave('capture_result.jpg',image)
	#		cv2.waitKey(0)
	#		cv2.destroyAllWindows()
	#	
	#		titles = ['Original Image','traffic','sign orginal','sign_ocr']
	#		images = [image,traffic,speed,sign]
	#		for i in xrange(4):
	#			cv2.imshow(titles[i],images[i])
	#	   		cv2.waitKey(0)
	#	    		cv2.destroyAllWindows()

			str2 = pytesseract.image_to_string(Image.open('speed_ocr_file.png'))	
	
			print("ocr is  ",str2)
			str2="{0:<8}".format(str2)
			str2=str2.strip()
		

			if str2 in ("START","5TART","STAI3T","SIART","SIARI","STARi","STAR}","STAR3"):
		
	              	#GPIO.output(18,True)  #LED
				GPIO.output(23,True)  #(pi -> FPGA)
				print('sending START to the client')
               		
	
			elif str2 in ( "STOP","SToP","ST0P","SlOP","STqP","QTQP","STC)P","ST()P","STc)P" ):
			
				GPIO.output(17,True)  #LED
				#GPIO.output(22,True)  #(pi -> FPGA)
				print('sending STOP to the client')
		
		#	if str2 in ( "SLOW","SLQW","Qlow","QlOW","SLOw","SLOVV","SLoW","SL0W","SLC)W","BLOW","SL()W") :
		#       elif str2 in ( "CURVE","OURVE","CUI3VE","CURUE","(URVE","CURVI"):
		#		print "okay3"
		#		GPIO.output(17,True)  #LED
		#		GPIO.output(22,True)  #(pi -> FPGA)
		#	elif str2 in ("60","6O","6o","6()","6C)","6c)"):
		#		print "okay4"
		#		GPIO.output(18,True)  #LED
		#		GPIO.output(23,True)  #(pi -> FPGA)		
		#	elif str2 in ("90","GO","6o","6()","6C)","6c)","G0","6O","go"):
		#     		print "okay4"
		#		GPIO.output(18,True)  #LED
		#		GPIO.output(23,True)  #(pi -> FPGA)
		#	elif str2 in ("CHARGE","C13ARGE","charge","CHA3GE","char9e","char0e"):
		#		print "charge station!"	
		#		GPIO.output(22,True)
	               
			else :
				print("pytesseract is NONE")
		
	except KeyboardInterrupt:
		camera.close()
		GPIO.cleanup()

		


def client_thread(conn, addr):
    print("Connected From : ", addr)
    while True:
        data = conn.recv(1024)
        #print data
        #TODO with Data
	
        print("[server]data ----------- "+data)
        res = do_some_stuffs_with_input(data)
        conn.sendall(res.encode("utf-8"))


if __name__ == '__main__':
    data2=""
    todo_thread = threading.Thread(target = server_work)
    todo_thread.start()
    
     # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     # Bind the socket to the port
    sock.bind((HOST, PORT))
     # Listen for incoming connections
     # Wait for a connection
    sock.listen(15)

 
    while True:
        conn, addr = sock.accept()
        client_thread = threading.Thread(target = client_thread, args = (conn, addr, ))
        client_thread.start()

    camera.close()








