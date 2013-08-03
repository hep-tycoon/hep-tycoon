
var API_ROOT = "http://localhost:5000";
var METHODS = [{"url": "/hr/scientists/", "args": [], "name": "list_scientists"}, {"url": "/", "args": [], "name": "index"}, {"url": "/hr/hire/<float:salary>/<int:n>", "args": ["salary", "n"], "name": "hire_scientists"}, {"url": "/hr/fire/<int:n>", "args": ["n"], "name": "fire_scientists"}, {"url": "/static/<path:filename>", "args": ["filename"], "name": "static"}];

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

function ajax_sugar(url, arg_names){
    var args = Array.prototype.slice.call(arguments, 2);
    url = url.replace(/<([^>]+)>/g, function(){
        return args.shift();
    });
    ajax("GET", url, args.shift());
}

function implement_ajax_sugar(){
    METHODS.forEach(function(method){
        window[method.name] = ajax_sugar.bind(this, method.url, method.args);
    });
}

implement_ajax_sugar();

