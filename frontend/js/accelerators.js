
function Accelerators($scope) {
    $scope.active = true;
    $scope.level = 1;
    $scope.description = "linear electron-positron collider";
    $scope.name = "LEP";
    $scope.energy = 42;
    $scope.cost = 200;

    $scope.shutdown = function(){
      shutdown_accelerator(function(){
        $scope.active = false;
        $scope.$apply();
      });
    };

    $scope.powerOn = function(){
      poweron_accelerator(function(){
        $scope.active = true;
        $scope.$apply();
      });
    };

    $scope.upgrade = function(){
      upgrade_accelerator(function(){
        $scope.update();
      });
    };

    $scope.update = function(){
      get_accelerator(function(res){
        angular.extend($scope, res);
        $scope.$apply();
      });
    };

    $scope.update();
}

