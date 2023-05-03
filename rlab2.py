import RPi.GPIO as GPIO
from time import sleep

pin = 18

farLeft = 3
farRight = 11

GPIO.setmode(GPIO.BCM) 			# Set the pin numbering to those on the board
GPIO.setup(pin, GPIO.OUT) 		# Set the chosen pin(18) to output mode

pwm = GPIO.PWM(pin,50) 			# Set up a 50Hz PWM signal on the chosen pin
pwm.start(7)

while(1):
	sleep(0.5)
	for i in range (3,11):
		pwm.ChangeDutyCycle(i)
		sleep(0.5)
	for j in range (11,3):
		pwm.ChangeDutyCycle(j)
		sleep(0.5)

sleep(1)
pwm.stop() 						#to stop PWM
GPIO.cleanup() 					# clean up GPIO channels that your script has used. Note #that GPIO.cleanup() also clears the pin numbering system