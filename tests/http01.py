import urllib2
import json
import threading

###############################################################################################
######################################################################### VARIABLES DECLARATION

# openweathermap API key
api_id = "57380854bce6937a9ab720e3440efe7c"

# See http://openweathermap.org/weather-conditions for weather codes
rain_codes = [ 200, 201, 202, 230, 231, 232, 						# thunderstorm
			   300, 301, 302, 310, 311, 312, 313, 314, 321,			# drizzle
			   500, 501, 502, 503, 504, 511, 520, 521, 522, 531,	# rain
			   600, 601, 602, 611, 612, 615, 616, 620, 621, 622,	# snow
			   901, 906]											# extreme

rain_status = False
poll_interval =  10 # 1800 # 1/2h

# 5 days forecast
# http://api.openweathermap.org/data/2.5/forecast?q=Paris,fr&mode=json

###############################################################################################
########################################################################### MAIN FUNCTIONS

# current weather conditions
def getCurrentWeatherCode():
	req = urllib2.Request('http://api.openweathermap.org/data/2.5/weather?q=Paris,fr&APPID=' + api_id)
	response = urllib2.urlopen(req)
	weather_data = response.read()
	decoded_data = json.loads(weather_data)

	global rain_status
	rain_status = searchForRainCode(decoded_data["weather"][0]["id"])

	print rain_status
	
###############################################################################################
########################################################################### UTILITIES FUNCTIONS

# search in the rain code list if the current weather code matches
def searchForRainCode(pWeatherCode):
	for c in rain_codes:
		if c == pWeatherCode:
			return True
	return False

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
set_interval( getCurrentWeatherCode, poll_interval )
getCurrentWeatherCode();