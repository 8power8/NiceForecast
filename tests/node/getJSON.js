(function(){

  var dataURL = 'http://api.openweathermap.org/data/2.5/forecast/daily?q=Paris,fr&mode=json&units=metric&cnt=2&APPID=57380854bce6937a9ab720e3440efe7c';

  var JSONDataGetterClass = require('./JSONDataGetter');
  var JSONDataGetter = JSONDataGetterClass.createInstance(dataURL);

  JSONDataGetter.getData();

  /*request(options, function (error, response, data) {
    if (!error && response.statusCode == 200) {
      console.log(data) // Print the google web page.
    }
    else
    {
      console.log('ERROR ! - satus code : ' + response.statusCode)
      console.log(error);
    }
  })*/

})();

