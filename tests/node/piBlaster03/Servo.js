var piblaster = require("pi-blaster.js");
var events = require('events');

// ######################################################## STATIC VARS
this.LEFT = 0.225;
this.CENTER = 0.138;
this.RIGHT = 0.048;

// ######################################################## CONSTRUCTOR
function Servo(pGPIONumber)
{
	this.GPIONumber = pGPIONumber;
}

// ######################################################## PRIVATE VARIABLES
var init = false;

var left = 0.230;
var center = 0.142;
var right = 0.050;

var lastPosition = center;
var position = center;
var I_moveServoTo;

Servo.prototype = new events.EventEmitter;

Servo.prototype.moveTo = function( pTo, pSpeed )
{

	var to = pTo;
	var stepWidth;
	var ms;

	switch(pSpeed)
	{

		case 1:
			stepWidth = 0.0006;
			ms = 40;
		break;

		case 2:
			stepWidth = 0.001;
			ms = 50;
		break;

		case 3:
			stepWidth = 0.0015;
			ms = 25;
		break;

		case 4:
			stepWidth = 0.008;
			ms = 50;
		break;

		case 5:
			stepWidth = 0.01;
			ms = 50;
		break;
	}

	I_moveServoTo = setInterval(function(context){

		if(lastPosition < to)
		{
			if(position < to)
			{
				position += stepWidth;
				piblaster.setPwm(context.GPIONumber, position);
			}
			else
			{
				clearInterval(I_moveServoTo);
				lastPosition = to;
				position = lastPosition;
				if(!init)
				{
					init = true;
					context.emit('initComplete', lastPosition);
				}
				else
				{
					context.emit('moveComplete', lastPosition);
				}
			}
		} 
		else if(lastPosition > to)
		{
			if(position > to)
			{
				position -= stepWidth;
				piblaster.setPwm(context.GPIONumber, position);
			}
			else
			{
				clearInterval(I_moveServoTo);
				lastPosition = to;
				if(!init)
				{
					init = true;
					context.emit('initComplete', lastPosition);
				}
				else
				{
					context.emit('moveComplete', lastPosition);
				}
			}
		}
		else
		{
			clearInterval(I_moveServoTo);
			if(!init)
				{
					init = true;
					context.emit('initComplete', lastPosition);
				}
				else
				{
					context.emit('noMoveNeeded', lastPosition);
				}
		}

	}, ms, this)
}

Servo.prototype.releasePin = function()
{
	piblaster.releasePin(this.GPIONumber)
}

// ######################################################## STATIC FUNCTIONS
exports.createInstance = function (pGPIONumber) 
{ 
	return new Servo(pGPIONumber);
}