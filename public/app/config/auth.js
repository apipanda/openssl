app.factory('Auth', ['$sessionStorage', '$localStorage', 'Request', '$window', '$q', function($sessionStorage, $localStorage, Request, $window, $q) {


    return {
        getAuth: function (auth) {
            // body...
            return $sessionStorage.get(auth);
        },
        $login: function (email, password) {
            // body...
            var endpoint = 'user/login';
            var payload = {
                email: email,
                password: password
            }
            Request.fetch(endpoint, payload)
                .then(function (status, result) {
                    console.log(status, result);
                }, function (code, err) {
                    // body...
                    console.log(code, err);
                });
        },
        $onAuth: function (cb) {
            // body...
            return !!cb;
        },
        $requireAuth: function () {
            var deferred = $q.defer();
            if (!!$sessionStorage.auth || !!$localStorage.auth && !!$localStorage.user) {
                deferred.resolve($localStorage.user);
            } else {
                deferred.reject("AUTH_REQUIRED");
            }
            return deferred.promise;
        },
        $logout: function () {
            // body...
            var endpoint = 'users/logout';
            var payload = {};
            Request.fetch(endpoint, payload, method='get')
                .then(function (resp) {
                    console.log(resp);
                    $localStorage.$reset();
                    $sessionStorage.$reset();
                    $window.location = '/';
                }, function (err) {
                    // body...
                    console.log(err);
                    $localStorage.$reset();
                    $sessionStorage.$reset();
                    $window.location.reload();
                });
        }
    }
  }]);