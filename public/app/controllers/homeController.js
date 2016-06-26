app.controller("HomeController", [
    "$scope",
    "$location",
    "$log",
    "Request",
    "domainBase",
    "verifyUrl",
    function ($scope, $location, $log, Request, domainBase, verifyUrl) {
        'use strict';

        $scope.verify = function () {
            var requestUrl = domainBase + verifyUrl;
            var data = $scope.domain;
            $scope.disableBtn = true;
            Request.fetch(requestUrl, data)
                .then(function (status, response, headers) {
                    // body...
                });

        };
        $log.info("Home Controller Initialized");
    }]);
