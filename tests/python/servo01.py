# Servo Control
# https://learn.adafruit.com/adafruits-raspberry-pi-lesson-8-using-a-servo-motor/software
# servo values for model PS-348 Pro 2
# 13 = --> (9h)
#	   
# 80 = ^ (12h)
#      |
#
# 153 = <-- (15)
#
# http://openweathermap.org/api
# openweathermap user : 8power8
# openweathermap API key : 57380854bce6937a9ab720e3440efe7c
#
# Python webservices : https://wiki.python.org/moin/WebServices


import time

def set(property, value):
	try:
		f = open("/sys/class/rpi-pwm/pwm0/" + property, 'w')
		f.write(value)
		f.close()	
	except:
		print("Error writing to: " + property + " value: " + value)
 
 
def setServo(angle):
	set("servo", str(angle))
	
		
set("delayed", "0")
set("mode", "servo")
set("servo_max", "180")
set("active", "1")
 
delay_period = 0.01
 
"""
while True:
	for angle in range(0, 180):
		setServo(angle)
		time.sleep(delay_period)
	for angle in range(0, 180):
		setServo(180 - angle)
		time.sleep(delay_period)
"""
while True:
	setServo(153)
	time.sleep(1)

	setServo(80)
	time.sleep(1)

	setServo(13)
	time.sleep(1)	