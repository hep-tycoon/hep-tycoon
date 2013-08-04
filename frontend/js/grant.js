function Grant($scope){
    $scope.papers = 0;
    $scope.total = 100;
    $scope.price = 0;

    $scope.getProgressbarStyle = function(){
        return {
            width: Math.round($scope.papers*100/$scope.total) + "%"
        };
    };
}

function setGrantInfo(papers, total, price){
    var $scope = $("#grant").scope();
    $scope.papers = papers;
    $scope.total = total;
    $scope.price = price;
    $scope.$apply();
}

