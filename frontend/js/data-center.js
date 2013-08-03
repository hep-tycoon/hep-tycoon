

function DataCenter($scope){
    $scope.usage = 31;
    $scope.capacity = 100;
    $scope.level = 1;

    $scope.upgrade = function(){
        // TODO
    };

    $scope.getProgressbarStyle = function(){
        return {
            width: Math.round($scope.usage*100/$scope.capacity) + "%"
        };
    };
}

