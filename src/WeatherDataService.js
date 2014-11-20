var request = require('request');
var http = require('http');
var events = require('events');

// ######################################################## CONSTRUCTOR
function WeatherDataService(pURL)
{
	this.options = {
		port: 80,
		method: 'GET'
  	};

  	this.options.url = pURL;
}

WeatherDataService.prototype = new events.EventEmitter;

// ######################################################## PUBLIC FUNCTIONS
WeatherDataService.prototype.getData = function() 
{
	var self = this;
	request(this.options, function (error, response, data) {
    if(!error && response.statusCode == 200) {
    	self.emit('onDataReceived', data);
    }
    else
    {
      console.log('ERROR ! - satus code : ' + response.statusCode)
      console.log(error);
    }
  })
}

// ######################################################## STATIC FUNCTIONS
exports.createInstance = function (pURL) 
{ 
	return new WeatherDataService(pURL);
}