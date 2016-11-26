app.controller("SwitchController", [
    "$scope",
    "$location",
    "$log",
    "$window",
    function ($scope, $location, $log, $window) {
        'use strict';

        $scope.hello = function () {
            // body...
            $window.alert("hELLO");
        };

        $log.debug("Switch Controller Initialized");
    }]);
