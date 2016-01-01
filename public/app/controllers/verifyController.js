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

        var expression = /[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?/gi;
        var regex = new RegExp(expression);

        function init() {
            // body...
            $scope.domainData = $localStorage.domain;

        }


        $scope.whois = function (forced) {
            forced = !!forced;

            $scope.error = null;
            $scope.warn = null;
            $scope.status = null;
            $scope.disableBtn = true;
            if (!!!$scope.domain.match(regex)) {
                $scope.error = "Your input is not a valid domain name.";
                $scope.status = 400;
            } else {
                var data = ($.url($scope.domain)).attr();
                var requestUrl = domainBase + whoisUrl;
                data.base = data.protocol ? data.base : 'http://' + data.base;
                data.forced = forced;

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
                        console.log(error);
                        $scope.error = "We cannot verify your domain at this time.";
                        // $scope.status = error.status + ' -';
                    });
            }

            $scope.disableBtn = false;

        };
        $scope.verify = function (type) {

            $scope.disableBtn = true;
            var requestUrl = domainBase + verifyUrl;
            var data = $scope.domainData;
            data.verification_type = type;

            Request.fetch(requestUrl, data)
                .then(function (response) {
                    // body...
                    if (!response.data.success) {
                        $scope.warn = response.message;
                        $scope.status = response.status + ' -';
                    } else {
                        console.log(response);
                        $localStorage.verified = response.data.success;
                        console.log(response);
                        $location.path('/signup');
                    }

                }, function (error) {
                    // body...
                    console.log(error);
                    alert('Cannot verify your domain name. Please try again');
                    $scope.error = "We've notified the developers.";
                    $scope.status = error.status + ' -';
                });
            $scope.disableBtn = false;

        }

        init();

        $log.debug("Verify Controller Initialized");
    }]);