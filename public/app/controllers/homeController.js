app.controller("HomeController", [
    "$scope",
    "$location",
    "$log",
    "$localStorage",
    "Request",
    "domainBase",
    "whoisUrl",
    function ($scope, $location, $log, $localStorage, Request, domainBase, whoisUrl) {
        'use strict';
        $scope.verify = function () {
            $scope.error = false;
            $scope.warn = false;
            $scope.status = null;
            $scope.disableBtn = true;
            var data = ($.url($scope.domain)).attr();
            var requestUrl = domainBase + whoisUrl;
            // console.log($scope.domain, data);
            Request.fetch(requestUrl, data)
                .then(function (response) {
                    // body...
                    if (!response.success) {
                        $scope.warn = response.message;
                        $scope.status = response.status + ' -';
                    }
                    $localStorage.domain = response.data;

                    $location.path('/verify');

                }, function (error) {
                    // body...
                    $scope.error = error.statusText;
                    $scope.status = error.status + ' -';
                });
            $scope.disableBtn = false;

        };

        $log.info("Home Controller Initialized");
    }]);
