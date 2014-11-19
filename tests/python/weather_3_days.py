import urllib2
import json
import pigpio

###############################################################################################
############################################################################## SERVO MANAGEMENT
pig = pigpio.pi()
pig.set_mode(7, pigpio.OUTPUT) # gpio 7 as output

left = 610
center = 1350
right = 2150

# left = 610, centre = 1350, right = 2150
def moveServoTo(pPosition):
	pig.set_servo_pulsewidth(7, pPosition)

###############################################################################################
##################################################################### WEATHER SERVICE FUNCTIONS
# openweathermap API key
api_id = "57380854bce6937a9ab720e3440efe7c"

# current weather conditions
def getRainForecastForNextHours(pNumHours):

	if(pNumHours < 3 or pNumHours > 72):
			print "pNumHours must be an integer between 3 and 120"
			return;

	req = urllib2.Request('http://api.openweathermap.org/data/2.5/forecast?q=Paris,fr&mode=json&APPID=' + api_id)
	response = urllib2.urlopen(req)
	weather_data = response.read()
	decoded_data = json.loads(weather_data)

	rainfall_mm = 0

	# for i in range(0, len(decoded_data["list"])): # this is for full list
	for i in range(0, pNumHours / 3):
		# rain key can be present or not in the object, so we must test for it's existence before using it
		try:
		    rainfall_mm += decoded_data["list"][i]["rain"]["3h"] # rain key exists in the current namespace
		    # print str(i) + " / " +  str(decoded_data["list"][i]["rain"]["3h"])
		except KeyError:
		    print "no rain key found!" # no rain key found

	print "The cumulated rainfall for the next "  + str(pNumHours) + " hours is " + str(rainfall_mm) + " mm"

	if rainfall_mm > 0:
		moveServoTo(right)
	else:
		moveServoTo(left)


###############################################################################################
######################################################################################### CALLS
getRainForecastForNextHours(3);