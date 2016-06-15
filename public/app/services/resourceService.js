/**
* resource Module
*
* Description
*/
app.service('Request', ['$http', 'API_URL', '$q', '$localStorage', 'promiseTracker', '$sessionStorage', function ($http, API_URL, $q, $localStorage, promiseTracker, $sessionStorage) {

        this.fetch = function (endpoint, obj, method, headers) {
            // body...
            var url = API_URL + endpoint;
            var data = obj || {};
            var auth = $sessionStorage.auth || $localStorage.auth || {};

            auth.tracker = this.estimatingTracker;
            $.extend(true, data, {
                source: 'web'
            });
            $.extend(true, headers, auth);

            var req = {
                method: method || 'post',
                url: url,
                data: angular.toJson(data, true),
                headers: headers
            };
            var defer = $q.defer();
            $http(req).then(function (res) {
                if (!!res.data.data) {
                    defer.resolve(res.data);
                } else{
                    defer.reject(res.data.error);
                };

            });
            return defer.promise;
        };
}]);