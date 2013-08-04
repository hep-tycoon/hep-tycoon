
angular.module("Tycoon", [])
    .filter("currency", ["$filter", function($filter){
        return function(input){
            return jetons(input, $filter);
        };
    }]);

function jetons(input, $filter) {
  input = Math.round(input) + ".";
  input = input.replace(/(\d)(?=(\d{3})+\.)/g, "$1,");
  return "JTN " + input.substring(0, input.length-1);
}

var startTime = null;
var GAME_SPEED = (60*60*24*365)/(30); // 30 seconds is one year
var START_DATE = new Date(1960, 6, 4).getTime();
var MONTHS = "Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec".split(",");
var $clock = $("#clock_target");

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

time(function(data){
    startTime = 1000*data.time;
    setInterval(updateClock, 250);
});

setInterval(function(){
    trigger(angular.noop);
}, 1000);

$('a[data-toggle=tooltip]').tooltip();
$('a[data-popover="hover"]').popover({ title: 'get title', content: 'get content from md', html: true, trigger: 'hover' });
