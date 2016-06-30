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
            console.log($scope.domain);
            var domain = ($.url($scope.domain)).attr();
            var requestUrl = domainBase + whoisUrl;
            var data = domain;
            $scope.disableBtn = true;
            Request.fetch(requestUrl, data)
                .then(function (response) {
                    // body...
                    console.log(response);
                }, function (error) {
                    // body...
                    console.log(error);
                });

        };
        $log.info("Home Controller Initialized");
    }]);
