app.controller("HomeController", [
    "$scope",
    "$location",
    "$log",
    "Request",
    "domainBase",
    "whoisUrl",
    function ($scope, $location, $log, Request, domainBase, whoisUrl) {
        'use strict';
        $log.debug(console.dir(Request.fetch));
        $scope.verify = function () {
            $scope.disableBtn = true;
            var data = ($.url($scope.domain)).attr();
            var requestUrl = domainBase + whoisUrl;
            console.log($scope.domain, data);
            Request.fetch(requestUrl, data)
                .then(function (response) {
                    // body...
                    console.log(response, 'response');
                }, function (error) {
                    // body...
                    console.log(error, 'errors');
                });
            $scope.disableBtn = false;

        };
        $log.info("Home Controller Initialized");
    }]);
