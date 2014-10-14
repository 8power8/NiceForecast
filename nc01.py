import urllib2
import json
import pigpio
import threading
import time
# import pygame

# pigpio init
pig = pigpio.pi()

# Servo values
servo_gpio = 7
mode_switch_gpio = 22
left = 610
center = 1350
right = 2150

# openweathermap API key
api_id = "57380854bce6937a9ab720e3440efe7c"

api_poll_interval = 1200 # 20 min

today_rain = 0
tomorrow_rain = 0

# switch mode GPIO
pig.set_mode(mode_switch_gpio, pigpio.INPUT)
#pig.set_pull_up_down(mode_switch_gpio, pigpio.PUD_OFF)

# servo GPIO
pig.set_mode(servo_gpio, pigpio.OUTPUT) 

time_stamp = time.time()


###############################################################################################
######################################################################## SWITCH MODE MANAGEMENT

# forecast mode
if pig.read(mode_switch_gpio) == 0:
	mode = "today"
elif pig.read(mode_switch_gpio) == 1:
	mode = "tomorrow"
else:
	mode = "today"

print "mode : " + mode

def onGPIO22RisingEdge(gpio, level, tick):
	global time_stamp
	global mode
	time_now = time.time()
	if (time_now - time_stamp) >= 0.2:
			mode = "tomorrow"
			moveServo()
	time_stamp = time_now

def onGPIO22FallingEdge(gpio, level, tick):
	global time_stamp
	global mode
	time_now = time.time()
	if (time_now - time_stamp) >= 0.2:
			mode = "today"
			moveServo()
	time_stamp = time_now


rise = pig.callback(22, pigpio.RISING_EDGE, onGPIO22RisingEdge)
fall = pig.callback(22, pigpio.FALLING_EDGE, onGPIO22FallingEdge)

###############################################################################################
############################################################################## SERVO MANAGEMENT

# Move the servo
def moveServo():
	print "moveServo"
	if mode == "today":
		print "today forecast"
		if today_rain > 0:
			pig.set_servo_pulsewidth(servo_gpio, left)
		else:
			pig.set_servo_pulsewidth(servo_gpio, right)
	elif mode == "tomorrow":
		print "tomorrow forecast"
		if tomorrow_rain > 0:
			pig.set_servo_pulsewidth(servo_gpio, left)
		else:
			pig.set_servo_pulsewidth(servo_gpio, right)

###############################################################################################
##################################################################### WEATHER SERVICE FUNCTIONS

# weather forecats infos
def getRainForecast():

	global today_rain
	global tomorrow_rain

	req = urllib2.Request('http://api.openweathermap.org/data/2.5/forecast/daily?q=Paris,fr&mode=json&units=metric&cnt=2&APPID=' + api_id)
	response = urllib2.urlopen(req)
	weather_data = response.read()
	decoded_data = json.loads(weather_data)
	response.close()

	# rain key can be present or not in the object, so we must test for it's existence before using it
	# if rain key is doesn't exists, it means no rain
	try:
	    today_rain = decoded_data["list"][0]["rain"] # rain key exists in the current namespace
	    print "today_rain = " + str(decoded_data["list"][0]["rain"]) + "mm"
	except KeyError:
		today_rain = 0 # no rain key found == no rain
		print "today_rain = 0"

	try:
	    tomorrow_rain = decoded_data["list"][1]["rain"] # rain key exists in the current namespace
	    print "tomorrow_rain = " + str(decoded_data["list"][1]["rain"]) + "mm"
	except KeyError:
		tomorrow_rain = 0 # no rain key found == no rain
		print "tomorrow_rain = 0" 

	time.sleep(2)
	moveServo()


###############################################################################################
################################################################################ SOUND HANDLING 

def playSound(pSoundFile):
		pygame.mixer.init()
		pygame.mixer.music.load(pSoundFile)
		pygame.mixer.music.play()
		while pygame.mixer.music.get_busy() == True:
		    continue
		pygame.mixer.music.stop();

###############################################################################################
########################################################################### UTILITIES FUNCTIONS

# setInterval wrapper
def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec) 
        func()  
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


###############################################################################################
######################################################################################### CALLS

pig.set_servo_pulsewidth(7, center)

time.sleep(2)

set_interval( getRainForecast, api_poll_interval )
getRainForecast();