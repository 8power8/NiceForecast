import pigpio
import threading
import time

# function to move a servo with custom speed

# Servo values
servo_gpio = 7
left = 2150
center = 1350
right = 610

initPosition = center

pig = pigpio.pi()
pig.set_mode(servo_gpio, pigpio.OUTPUT)

pig.set_servo_pulsewidth(servo_gpio, center)
currentPosition = initPosition
time.sleep(1)



def moveServoTo(pServoGPIO, pTo, pSpeed = 5):

	if pSpeed == 5:
		step = 10
		ms = 0.002
	elif pSpeed == 4:
		step = 6
		ms = 0.004
	elif pSpeed == 3:
		step = 4
		ms = 0.01
	elif pSpeed == 2:
		step = 3
		ms = 0.01
	elif pSpeed == 1:
		step = 1
		ms = 0.01
	else:
		step = 10
		ms = 0.002

	try:
		global currentPosition

		if(pTo >= currentPosition):
			while currentPosition <= pTo:
				currentPosition += step
				pig.set_servo_pulsewidth(pServoGPIO, currentPosition)
				time.sleep(ms)
		elif(pTo <= currentPosition):
			while currentPosition >= pTo:
				currentPosition -= step
				pig.set_servo_pulsewidth(pServoGPIO, currentPosition)
				time.sleep(ms)
	except KeyboardInterrupt:
				pig.set_servo_pulsewidth(pServoGPIO, 0)

moveServoTo(servo_gpio, left, 5)
