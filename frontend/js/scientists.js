
function Scientists($scope){

    $scope.updateEmployees = function(){
        list_scientists(function(data){
            $scope.scientists = data.scientists;
            $scope.maxScientists = data.max_scientists;
            $scope.slots = $scope.maxScientists - $scope.scientists.length;
            $scope.$apply();
        });
    };

    $scope.hire = function(){
        hire_scientists(
            $scope.hireScientistsCount,
            function(){
                $("#modConfirmHire").modal("hide");
                $scope.updateEmployees();
            }
        );
    };

    $scope.setHireCount = function(count){
      $scope.hireScientistsCount = count;
    }

    $scope.fire = function(){
        fire_scientists(
            $scope.fireScientistsCount,
            function(){
                $("#modConfirmFire").modal("hide");
                $scope.updateEmployees();
            }
        );
    };

    $scope.setFireCount = function(count){
      $scope.fireScientistsCount = count;
    }

    $scope.adjustSalary = function(){
        set_salary(
            $scope.hireScientistsCostNew,
            function(){
                $scope.hireScientistsCost = $scope.hireScientistsCostNew;
                $scope.$apply();
            }
        );
    };

    $scope.fireScientistsCost = 1000;
    $scope.hireScientistsCost = 1000;
    $scope.hireScientistsCostNew = 1000;
    $scope.updateEmployees();

}

function updateScientists(){
    $("#staff").scope().updateEmployees();
}

