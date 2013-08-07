
function Accelerators($scope) {
    $scope.active = false;
    $scope.level = 1;
    $scope.name = '';
    $scope.energy = 42;
    $scope.running_costs = 200;
    $scope.docs = ''

    $scope.power = function(){
      if ($scope.active)
        shutdown_accelerator($scope.$apply);
      else
        poweron_accelerator($scope.$apply);
    };
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
        readTextFile(DOCS_DIR + 'accelerators/' + $scope.geometry + '/' + $scope.particles + '/' + $scope.level + '.html', function (result) { $scope.docs = result; } );
        $scope.$apply();
      });
    };

    $scope.getPowerButtonClass = function(){
      if ($scope.active)
        return 'btn btn-danger'
      return 'btn btn-success'
    }

    $scope.getPowerButtonText = function(){
      if ($scope.active)
        return '<span class="glyphicon glyphicon-off"></span> Shut down';
      return '<span class="glyphicon glyphicon-off"></span> Run';
    }

    $scope.update();
}

function setAcceleratorInfo(active){
    var $scope = $("#accelerator").scope();
    $scope.active = active;
    $scope.$apply();
}

