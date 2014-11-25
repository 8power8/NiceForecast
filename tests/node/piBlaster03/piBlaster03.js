(function(){

  var ServoClass = require('./Servo');
  var Gpio = require('onoff').Gpio;
  //var piblaster = require("pi-blaster.js");
  var buttonState;

var LEFT = 0.225;
var CENTER = 0.138;
var RIGHT = 0.048;

  // ################################################################# SWITCH BUTTON HANDLING
  var switchButton = new Gpio(22, 'in', 'both', {debounceTimeout : 0});
  buttonState = switchButton.readSync();

  switchButton.watch(function(err, value) 
  {
      if (err) throw err;
      if(value != buttonState)
      {
        buttonState = value;
        console.log('Button state changed to ' + value);
        updateUI();
      }
      
  });


  // ################################################################# SERVO HANDLING
  var servo = ServoClass.createInstance(4);

  servo.on('moveComplete', function(pPosition){
    console.log('move complete pos = ' + pPosition);
  });

  servo.on('noMoveNeeded', function(pPosition){
    console.log('no move needed pos = ' + pPosition);
  });

  servo.moveTo(RIGHT, 1);

  // ################################################################# OTHER FUNCTIONS
  function updateUI()
  {
    if(buttonState == 0) // today
    {
      //piblaster.setPwm(4, 0.230);
    }
    else
    {
       //piblaster.setPwm(4, 0.050);
    }
  }

  //piblaster.setPwm(4, 0.142);

})();

