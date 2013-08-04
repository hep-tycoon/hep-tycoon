
function Detectors($scope){
    $scope.max_detectors = 0;
    $scope.detectors = [];
    $scope.free_slots = 0;

    $scope.update = function(){
        get_detectors(function(data){
            $scope.detectors = data.detectors;
            $scope.free_slots = data.free_slots;
            $scope.availableDetectors = data.available;
            $scope.max_detectors = data.max_detectors;
            $scope.$apply();
        });
    };

    $scope.upgrade = function(slug){
        upgrade_detector(slug, function(){
            $scope.update();
            updateScientists();
        });
    };
    $scope.remove = function(slug){
        remove_detector(slug, function(){
            $scope.update();
            updateScientists();
        });
    };

    $scope.install = function(slug){
        $("#modDetectors").modal("hide");
        buy_detector(slug, function(){
            $scope.update();
            updateScientists();
        });
    };

    $scope.btngroupclass = function(can_upgrade){
        if(can_upgrade) return 'pull-right btn-group';
        return 'pull-right';
    }

    $scope.slots = function(slots){
        if(slots == 1) return 'slot';
        return 'slots';
    }

    $scope.update();
}

function updateDetectors(){
    $("#detectors").scope().update();
}

