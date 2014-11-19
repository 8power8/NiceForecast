(function(){

  var dataURL = 'http://api.openweathermap.org/data/2.5/forecast/daily?q=Paris,fr&mode=json&units=metric&cnt=2&APPID=57380854bce6937a9ab720e3440efe7c';

  // ################################################################# SWITCH BUTTON HANDLING
  var Gpio = require('onoff').Gpio;
  var switchButton = new Gpio(22, 'in', 'both', {debounceTimeout : 0});
  var state = switchButton.readSync();

  switchButton.watch(function(err, value) 
  {
      if (err) throw err;
      if(value != state)
      {
        state = value;
        console.log('Button state changed to ' + value);
      }
      
  });

  // ################################################################# REMOTE JSON DATA HANDLING
  var JSONDataGetterClass = require('./JSONDataGetter');
  var JSONDataGetter = JSONDataGetterClass.createInstance(dataURL);

  JSONDataGetter.on('onDataReceived', function(pData){
    console.log(pData);
  });

  // ################################################################# EXECTUTION
  if(state == 0)
  {
    // get the today data
  }
  else
  {
  // get the tomorrow data
  }
  //JSONDataGetter.getData();


})();

