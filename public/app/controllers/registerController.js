app.controller("RegisterController", [
    "$scope",
    "$location",
    "$log",
    "$localStorage",
    "$sessionStorage",
    "$rootScope",
    "Request",
    function ($scope, $location, $log, $localStorage, $sessionStorage, $rootScope, Request) {
        'use strict';

        if (!$localStorage.domain && !$localStorage.verified) {
            $location.path('/login');
        };

        $scope.data = {};

        $scope.register = function () {
            $scope.message = null;
            var data = $localStorage.domain
            $scope.data.domain = {
                domain_name: data.org || data.host,
                domain_url: $localStorage.domain.host,
                domain_registrar: data.registrar,
                date_registered: data.creation_date,
                expiration_date: data.expiration_date,
                verification_type: data.verification_type
            };

            var errCode;
            Request.fetch('users', $scope.data)
                .then(function (res) {
                    $sessionStorage.auth = res.auth;
                    $localStorage.auth = res.auth;
                    $localStorage.user = res.data;
                    $rootScope.user = $localStorage.user;
                    $location.path('/dashboard')
                }, function (error) {
                    console.log(error);
                    $scope.message = error.message;

                });

        }
        $log.debug("Register Controller Initialized");
    }]);