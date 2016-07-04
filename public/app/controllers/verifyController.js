app.controller("VerifyController", [
    "$scope",
    "$location",
    "$log",
    "$localStorage",
    "Request",
    "domainBase",
    "whoisUrl",
    "verifyUrl",
    function ($scope, $location, $log, $localStorage, Request, domainBase, whoisUrl, verifyUrl) {
        'use strict';
        if (!!!$localStorage.domain) {
            $location.path('/');
        }

        $scope.whois = function () {
            $scope.error = null;
            $scope.warn = null;
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

        $log.debug("Verify Controller Initialized");
    }]);
