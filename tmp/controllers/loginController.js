app.controller("LoginController", [
    "$scope",
    "$location",
    "$log",
    "$localStorage",
    "$sessionStorage",
    "$rootScope",
    "Request",
    function ($scope, $location, $log, $localStorage, $sessionStorage, $rootScope, Request) {
        'use strict';
        $scope.login = function (email, password) {
            $scope.message = null;
            var endpoint = 'users/login';
            var data = {
                email: email,
                password: password
            };

            Request.fetch(endpoint, data)
                .then(function (res) {
                    $sessionStorage.auth = res.auth;
                    $localStorage.auth = res.auth;
                    $localStorage.user = res.data;
                    $rootScope.user = $localStorage.user;
                    $location.path('/dashboard');

                }, function (error) {
                    console.log(error.code);
                    var errCode = error.code.split('_').join(' ');
                    $scope.errCode = errCode.substring(0,1).toUpperCase() + errCode.substring(1).toLowerCase() + "!";
                    $scope.message = error.message;
                    console.log(errCode, $scope.errCode, $scope.message);
                });
        }
        $log.debug("Login Controller Initialized");
    }]);
