

function Scientists($scope){
    $scope.updateEmployees = function(){
        list_scientists(function(data){
            $scope.scientists = data.scientists;
            $scope.$apply();
        });
    };

    $scope.hire = function(){
        hire_scientists(
            $scope.hireScientistsCost,
            $scope.hireScientistsCount,
            function(){
                $("#modConfirmHire").modal("hide");
                $scope.updateEmployees();
            }
        );
    };

    $scope.fire = function(){
        fire_scientists(
            $scope.fireScientistsCount,
            function(){
                $("#modConfirmFire").modal("hide");
                $scope.updateEmployees();
            }
        );
    };

    $scope.maxScientists = 100;
    $scope.fireScientistsCost = 1000;
    $scope.hireScientistsCost = 1000;
    $scope.updateEmployees();

}

