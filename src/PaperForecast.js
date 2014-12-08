(function(){

  var xmldoc = require('xmldoc');
  var ServoClass = require('./Servo'); 
  var dataURL = 'http://api.openweathermap.org/data/2.5/forecast/daily?q=Paris,fr&mode=xml&units=metric&cnt=7&APPID=57380854bce6937a9ab720e3440efe7c';
  var todayRain;
  var tomorrowRain;
  var buttonState;

  var LEFT = 0.225;
  var CENTER = 0.138;
  var RIGHT = 0.048;

  // ################################################################# SWITCH BUTTON HANDLING
  var Gpio = require('onoff').Gpio;
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

  // ################################################################# REMOTE JSON DATA HANDLING
  var WeatherDataServiceClass = require('./WeatherDataService');
  var weatherDataService = WeatherDataServiceClass.createInstance(dataURL);

  weatherDataService.on('onDataReceived', function(pData){
    var xmlData = new xmldoc.XmlDocument(pData);
    var forecast = xmlData.childNamed("forecast");

    var today = forecast.children[0].children[1].attr.value;
    var tomorrow = forecast.children[1].children[1].attr.value;

    today ? todayRain = parseFloat(today) : todayRain = 0;
    tomorrow ? tomorrowRain = parseFloat(tomorrow) : tomorrowRain = 0;

    console.log('weather data ok', 'today: ' + todayRain + ' mm', 'tomorrow: ' + tomorrowRain + ' mm');

    //updateUI();

    //servo.init();

  });

  weatherDataService.getData();

  // ################################################################# SERVO HANDLING
  var servo = ServoClass.createInstance(4);

  servo.on('moveComplete', function(pPosition){
    console.log('move complete pos = ' + pPosition);
  });

  servo.on('noMoveNeeded', function(pPosition){
    console.log('no move needed pos = ' + pPosition);
  });

  servo.moveTo(CENTER);

  // ################################################################# OTHER FUNCTIONS
  function updateUI()
  {

    if(buttonState == 0) // today
    {
      servo.moveTo(LEFT);
    }
    else // tomorrow
    {
      servo.moveTo(RIGHT);
    }

    /*if(buttonState == 0) // today
    {
      if(todayRain == 0)
      {
        servo.moveTo(0.214, 2);
      }
      else
      {
         servo.moveTo(0.062, 2);
      }
    }
    else // tomorrow
    {
      if(tomorrowRain == 0)
      {
        servo.moveTo(0.214, 2);
      }
      else
      {
         servo.moveTo(0.062, 2);
      }
    }*/
  }


})();

