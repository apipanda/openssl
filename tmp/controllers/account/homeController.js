app.controller("DashController", [
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

        $log.debug("Dash Controller Initialized");
    }]);
