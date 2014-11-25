var piblaster = require("pi-blaster.js");

var left = 0.225;
var center = 0.138;
var right = 0.048;


var lastPosition = center;
var position = center;
var I_moveServoTo;

piblaster.setPwm(4, center);

function moveTo( pTo, pSpeed )
{

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

	I_moveServoTo = setInterval(function(){

		if(lastPosition < pTo)
		{
			if(position < pTo)
			{
				position += stepWidth;
				piblaster.setPwm(4, position);
			}
			else
			{
				clearInterval(I_moveServoTo);
				lastPosition = pTo;
				position = lastPosition;
			}
		} 
		else if(lastPosition > pTo)
		{
			if(position > pTo)
			{
				position -= stepWidth;
				piblaster.setPwm(4, position);
			}
			else
			{
				clearInterval(I_moveServoTo);
				lastPosition = pTo;
			}
		}

	}, ms)
}

//setTimeout(function(){moveTo(right, 1)}, 2000);