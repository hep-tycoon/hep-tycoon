
function DataCenter($scope){
    $scope.usage = 0;
    $scope.capacity = 1;
    $scope.level = 0;
    $scope.max_level = 0;

    $scope.upgrade = function(){
        upgrade_datacenter(function(){
            $scope.update();
        });
    };

    $scope.update = function(){
        get_datacenter(function(datacenter){
            angular.extend($scope, datacenter);
            $scope.$apply();
        });
    };

    $scope.getProgressbarStyle = function(){
        return {
            width: Math.round($scope.usage*100/$scope.capacity) + "%"
        };
    };

    $scope.update();
}

