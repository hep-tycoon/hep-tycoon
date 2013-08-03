
var API_ROOT = "";
var METHODS = [{"url": "/accelerator/shutdown", "args": [], "name": "shutdown_accelerator"}, {"url": "/accelerator/poweron", "args": [], "name": "poweron_accelerator"}, {"url": "/accelerator/upgrade", "args": [], "name": "upgrade_accelerator"}, {"url": "/datacenter/upgrade", "args": [], "name": "upgrade_datacenter"}, {"url": "/hr/scientists/", "args": [], "name": "list_scientists"}, {"url": "/accelerator", "args": [], "name": "get_accelerator"}, {"url": "/datacenter", "args": [], "name": "get_datacenter"}, {"url": "/detectors", "args": [], "name": "get_detectors"}, {"url": "/time", "args": [], "name": "time"}, {"url": "/", "args": [], "name": "index"}, {"url": "/hr/hire/<float:salary>/<int:n>", "args": ["salary", "n"], "name": "hire_scientists"}, {"url": "/hr/salary/<float:newsalary>", "args": ["newsalary"], "name": "set_salary"}, {"url": "/hr/fire/<int:n>", "args": ["n"], "name": "fire_scientists"}, {"url": "/frontend/<path:filename>", "args": ["filename"], "name": "static"}];

function ajax(method, object, callback) {
    $.ajax({
        url : API_ROOT + object,
        type: method,
        dataType: "json"
    }).done(function(data){
        callback(data);
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

