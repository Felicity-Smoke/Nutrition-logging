import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)







GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
while 1:
	print 'LED y on'
	GPIO.output(19, GPIO.HIGH)
	time.sleep(2)
	print 'LED y off'
	GPIO.output(19,GPIO.LOW)
	time.sleep(0.5)
	print 'LED on'
	GPIO.output(26, GPIO.HIGH)
	time.sleep(2)
	GPIO.output(26, GPIO.LOW)
	print 'LED off'
	time.sleep(0.5)