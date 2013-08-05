
function Accelerators($scope) {
    $scope.active = false;
    $scope.level = 1;
    $scope.name = "LEP";
    $scope.energy = 42;
    $scope.running_costs = 200;

    $scope.shutdown = function(){
      shutdown_accelerator(function(){
        $scope.$apply();
      });
    };

    $scope.powerOn = function(){
      poweron_accelerator(function(){
        $scope.$apply();
      });
    };

    $scope.upgrade = function(){
      upgrade_accelerator(function(){
        $scope.update();
        updateScientists();
        updateDetectors();
      });
    };

    $scope.update = function(){
      get_accelerator(function(res){
        angular.extend($scope, res);
        readTextFile(DOCS_DIR + 'accelerators/' + $scope.geometry + '/' + $scope.particles + '/' + $scope.level + '.html', function (result) { $('div[data-docs="accelerator"]').html(result); } );
        $scope.$apply();
      });
    };

    $scope.update();
}

function setAcceleratorInfo(active){
    var $scope = $("#accelerator").scope();
    $scope.active = active;
    $scope.$apply();
}

