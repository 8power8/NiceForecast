import urllib2
import json

###############################################################################################
##################################################################### WEATHER SERVICE FUNCTIONS
# openweathermap API key
api_id = "57380854bce6937a9ab720e3440efe7c"
forecast_hours_length = 3
api_poll_interval = 10 # 1800 # 1/2h

today_rain = 0
tomorrow_rain = 0

# weather forecats infos
def getRainForecast():

	global today_rain
	global tomorrow_rain

	req = urllib2.Request('http://api.openweathermap.org/data/2.5/forecast/daily?q=Paris,fr&mode=json&units=metric&cnt=2')
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

	

getRainForecast()