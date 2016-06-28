app.controller("BlogController", [
    "$scope",
    "$location",
    "$log",
    "$window",
    function ($scope, $location, $log, $window) {
        'use strict';
        this.postList = $window.postList;
        this.postLength = $window.postList.length;
        console.log(this);
        $log.debug("Blog Controller Initialized");
    }]);
