
var funds = 0;

angular.module("Tycoon", [])
    .filter("currency", ["$filter", function($filter){
        return function(input){
            return jetons(input, $filter);
        };
    }])
    .directive("disableCost", function(){
        return function(scope, $elm, attrs){
            var price = attrs.disableCost;

            var unwatch = scope.$watch(function(){
                return funds;
            }, function(){
                var price = attrs.disableCost;
                $elm[price>funds?"attr":"removeAttr"]("disabled", "1");
            });
            $elm.bind("$destroy", unwatch);
        };
    });

function jetons(input, $filter) {
  input = Math.round(input) + ".";
  input = input.replace(/(\d)(?=(\d{3})+\.)/g, "$1,");
  return "JTN " + input.substring(0, input.length-1);
}

var startTime = null;
var GAME_SPEED = (60*60*24*365)/(30); // 30 seconds is one year
var START_DATE = new Date(1960, 6, 4).getTime();
var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
var $clock = $("#clock_target");

var DOCS_DIR = '/frontend/docs/';

function formatDate(date){
  var month = MONTHS[date.getMonth()];
  var day = "0" + date.getDate();
  day = day.substring(day.length-2);
  return month + " " + date.getFullYear();
}

function updateClock(){
  var elapsed = new Date() - startTime;
  var gameTime = new Date(START_DATE + elapsed*GAME_SPEED);
  $clock.text(formatDate(gameTime));
}

function readTextFile(file, callback)
{
    $.ajax({
            url : file,
            success : callback
    });
}

time(function(data){
    startTime = 1000*data.time;
    setInterval(updateClock, 250);
});

setInterval(function(){
    if(funds >= 0){
      trigger(angular.noop);
    }
}, 1000);

$('a[data-toggle=tooltip]').tooltip();
