
function Accelerators($scope) {
    $scope.active = true;
    $scope.level = 1;
    $scope.description = "linear electron-positron collider";
    $scope.name = "LEP";
    $scope.energy = 42;
    $scope.cost = 200;

    $scope.shutdown = function(){
      $scope.active = false;
    };

    $scope.powerOn = function(){
      $scope.active = true;
    };
}

