

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

