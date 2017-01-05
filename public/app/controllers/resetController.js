app.controller("ResetController", [
    "$scope",
    "$location",
    "$log",
    function ($scope, $location, $log) {
		'use strict';
		$scope.message = false;

		$log.debug("Reset Controller Initialized");
    }]);