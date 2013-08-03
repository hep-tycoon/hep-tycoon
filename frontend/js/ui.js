

$("#hireScientistsBtn").click(function(){
    hire_scientists(
        "2000.0",
        $("#iHireScientists").val(),
        function(){
            $("#modConfirmHire").modal("hide");
            $("#iHireScientists").val("");
            updateEmployees();
        }
    );
});

$("#iFireScientistsBtn").click(function(){
    fire_scientists(
        $("#iFireScientistsInput").val(),
        function(){
            $("#modConfirmFire").modal("hide");
            updateEmployees();
        }
    );
});

function updateEmployees(){
    list_scientists(function(data){
        var scientists = data.scientists;
        $("#iScientistCount").text(scientists.length);
        var $target = $("#iScientistsList").empty();
        scientists.forEach(function(name){
            $target.append(
                $("<tr/>").append("<td/>").text(name)
            );
        });
    });
}

updateEmployees();




