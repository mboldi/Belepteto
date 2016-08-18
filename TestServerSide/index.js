var express = require('./')
var app = express();

app.post('/', function(req, res){
  res.send('got "' + req.text + '"');
});

app.listen(3000)