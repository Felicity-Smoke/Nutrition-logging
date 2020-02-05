import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 16
GPIO_ECHO = 18

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

CONNECTION_STRING ="mongodb://iotdbtechdays:ph8XzIZOuyYwUPUPUMWbxi2HNMPBv3hWGg3fp7opatv5nWp5HhAIGXSPlbHtoxAfWNHfYQeJcEq8DaSjyrgSGA==@iotdbtechdays.documents.azure.com:10255/?ssl=true&replicaSet=globaldb"

def distance():
        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
        StartTime=time.time()
        StopTime=time.time()
        while GPIO.input(GPIO_ECHO)==0:
                StartTime=time.time()
        while GPIO.input(GPIO_ECHO)==1:
                StopTime = time.time()
        TimeElapsed = StopTime - StartTime
        return (TimeElapsed * 34300) / 2
if __name__ == "__main__":
        try:
                while True:
                        dist = distance()
                        print ('Distance: %.1f' % dist)
                        time.sleep(1)
        except KeyboardInterrupt:
                print ('Measurement stopped by user')
                GPIO.cleanup()
