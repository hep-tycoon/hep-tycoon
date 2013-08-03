
var API_ROOT = "";
var METHODS = [{"url": "/accelerator/shutdown", "args": [], "name": "shutdown_accelerator"}, {"url": "/accelerator/poweron", "args": [], "name": "poweron_accelerator"}, {"url": "/accelerator/upgrade", "args": [], "name": "upgrade_accelerator"}, {"url": "/datacenter/upgrade", "args": [], "name": "upgrade_datacenter"}, {"url": "/hr/scientists/", "args": [], "name": "list_scientists"}, {"url": "/accelerator", "args": [], "name": "get_accelerator"}, {"url": "/datacenter", "args": [], "name": "get_datacenter"}, {"url": "/detectors", "args": [], "name": "get_detectors"}, {"url": "/funds", "args": [], "name": "funds"}, {"url": "/time", "args": [], "name": "time"}, {"url": "/", "args": [], "name": "index"}, {"url": "/detector/<detector>/upgrade", "args": ["detector"], "name": "upgrade_detector"}, {"url": "/detector/<detector>/remove", "args": ["detector"], "name": "remove_detector"}, {"url": "/detector/<detector>/add", "args": ["detector"], "name": "buy_detector"}, {"url": "/hr/salary/<float:newsalary>", "args": ["newsalary"], "name": "set_salary"}, {"url": "/hr/hire/<int:n>", "args": ["n"], "name": "hire_scientists"}, {"url": "/hr/fire/<int:n>", "args": ["n"], "name": "fire_scientists"}, {"url": "/frontend/<path:filename>", "args": ["filename"], "name": "static"}];

function ajax(method, object, callback) {
    $.ajax({
        url : API_ROOT + object,
        type: method,
        dataType: "json"
    }).done(function(data){
        $("#iFunds").text(jetons(data.gameStatus.funds));
        callback(data.response);
    }).error(function(){
        alert("Error"); // TODO: nicer errors
        console.log(arguments);
    });
}

function format(type, val){
    val += "";
    switch(type){
        case "int":
            if(!/^\d+$/.test(val)){
                throw "Invalid int " + val;
            }
            return val;
        case "float":
            if(!~val.indexOf(".")){
                val += ".0";
            }
            if(!/^\d+\.\d+$/.test(val)){
                throw "Invalid float " + val;
            }
            return val;
    }
    throw "Undefined type " + type;
}

function ajax_sugar(url, arg_names){
    var args = Array.prototype.slice.call(arguments, 2);
    url = url.replace(/<([^>]+)>/g, function(_, name){
        var val = args.shift();
        var pos = name.indexOf(":");
        if(pos > 0){
            var type = name.substring(0, pos);
            val = format(type, val);
        }
        return val;
    });
    ajax("GET", url, args.shift());
}

function implement_ajax_sugar(){
    METHODS.forEach(function(method){
        window[method.name] = ajax_sugar.bind(this, method.url, method.args);
    });
}

implement_ajax_sugar();

