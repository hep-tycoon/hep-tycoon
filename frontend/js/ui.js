
angular.module("Tycoon", [])
    .filter("currency", ["$filter", function($filter){
        return function(input){
            return jetons(input, $filter);
        };
    }]);

function jetons(input, $filter) {
  var curSymbol = curSymbol || "JTN ";
  var decPlaces = decPlaces || 0;
  var thouSep = thouSep || ",";
  var decSep = decSep || ".";

  // Check for invalid inputs
  var out = isNaN(input) || input === '' || input === null ? 0.0 : input;

  //Deal with the minus (negative numbers)
  var minus = input < 0;
  out = Math.abs(out);
  out = $filter("number")(out, decPlaces);

  // Replace the thousand and decimal separators.  
  // This is a two step process to avoid overlaps between the two
  if(thouSep != ",") out = out.replace(/\,/g, "T");
  if(decSep != ".") out = out.replace(/\./g, "D");
  out = out.replace(/T/g, thouSep);
  out = out.replace(/D/g, decSep);

  // Add the minus and the symbol
  if(minus){
    return "-" + curSymbol + out;
  }else{
    return curSymbol + out;
  }
}

var startTime = new Date();
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
  var elapsed = (new Date() - startTime);
  var gameTime = new Date(START_DATE + elapsed*GAME_SPEED);
  $clock.text(formatDate(gameTime));
}
setInterval(updateClock, 250);

$('a[data-toggle=tooltip]').tooltip();
$('a[data-popover="hover"]').popover({ title: 'get title', content: 'get content from md', html: true, trigger: 'hover' });
