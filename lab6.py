#Shivam Kundan
#ECE 296, Fall 2016
#Raspberry Pi Lab #6

#Program to implement a radar using a servo, ultrasonic sensor, and LCD.

import signal
import RPi.GPIO as GPIO
from myLCD import*
from time import *

GPIO.setmode(GPIO.BCM) 			# Set the pin numbering to those on the board


leftArrow=[0x00,0x00,0x04,0x08,0x1F,0x08,0x04,0x00]	#0
leftUpArrow=[0x1D,0x18,0x14,0x12,0x01,0x00,0x00,0x00]	#1
upArrow=[0x04,0x0E,0x15,0x04,0x04,0x04,0x04,0x04]	#2
rightUpArrow=[0x0F,0x03,0x05,0x09,0x10,0x00,0x00,0x00]	#3
rightArrow=[0x00,0x00,0x04,0x02,0x1F,0x02,0x04,0x00]	#4



Arr=[0,0,0,0,0] #Saves the state of LCD's line 1 (keep track of arrows)


#--------------------------------Function for Sensor Use---------------------------
def printArrows():
	disp=''
	global Arr
	for j in range (0,5):
		if(Arr[j]): disp=disp+'chr('+j+')'
	lcd_string(GPIO,disp,1)



def sensor(i):
	#Generate pulse
	GPIO.output(outpin,False)
	sleep(0.01)
	GPIO.output(outpin,True)
	sleep(0.01)
	GPIO.output(outpin,False)


	#Wait for pulse to be received back
	while(GPIO.input(inpin)==False):
		pass	#Do nothing
	
	starttime=time()
	
	while(GPIO.input(inpin)==True):
		pass	#Do nothing

	stoptime=time()
	
	elapsedtime=float(stoptime - starttime)
	dist=100*(343*elapsedtime)/2		#in centimeters

	if(dist<100):
		if (i==3): Arr[0]=1 
		if (i==5): Arr[1]=1
		if (i==7): Arr[2]=1
		if (i==9): Arr[3]=1
		if (i==11):Arr[4]=1
	printArrows()
	lcd_string(GPIO,str(dist),2)		#print distance to lcd
#---------------------------------------------------------------------------------

#Set servo
pin = 18
farLeft = 3
farRight = 11
GPIO.setup(pin, GPIO.OUT) 		# Set the chosen pin(18) to output mode
pwm = GPIO.PWM(pin,50) 			# Set up a 50Hz PWM signal on the chosen pin

#Set ultrasound sensor pins
inpin=24		#Echo
outpin=23		#Trigger
GPIO.setup(inpin, GPIO.IN) 
GPIO.setup(outpin, GPIO.OUT) 	
pwm.start(7)

#Set LCD Pins
D4=25
D5=12	
D6=16
D7=21
RS=4
E=17
BKL=True

#Initialize LCD 
start(GPIO,2,16)
LCD(GPIO,RS,E,D4,D5,D6,D7,BKL)
lcd_init(GPIO)

lcd_custom(GPIO,0,leftArrow)
lcd_custom(GPIO,1,leftUpArrow)
lcd_custom(GPIO,2,upArrow)
lcd_custom(GPIO,3,rightUpArrow)
lcd_custom(GPIO,4,rightArrow)


#---------------------------------Signal Handling---------------------------------
def signal_handler(signal,frame):
	lcd_string(GPIO,'End of Program',1)
	lcd_string(GPIO,'      Bye!',2)
	sleep(3)
	lcd_shutdown(GPIO)	
	GPIO.cleanup() 					# clean up GPIO channels
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
#---------------------------------------------------------------------------------


#Begin main loop
while(1):
	Arr=[0,0,0,0,0]
	sleep(0.5)
	for i in range(3,11):
		pwm.ChangeDutyCycle(i)
		print(i)
		sleep(0.5)
		sensor(i)	#Use the sensor


	Arr=[0,0,0,0,0]
	sleep(0.5)
	for i in range(11,3,-1):
		pwm.ChangeDutyCycle(i)
		print(i)
		sleep(0.5)
		sensor(i)	#Use the sensor


sleep(1)


lcd_shutdown(GPIO)	
GPIO.cleanup() 					# clean up GPIO channels


