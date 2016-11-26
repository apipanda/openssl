app.service('LocationService', ["$http", "$q", function ($http, $q) {
    'use strict';
    return {
        listLocations: function () {
            var defer = $q.defer();
            $http({
                method: "GET",
                url: "api/location/"
            }).success(function (data, status, headers, config) {
                defer.resolve(data);
            }).error(function (data, status, headers, config) {
                defer.reject(status);
            });
            return defer.promise;
        },
        getLocation: function (id) {
            var defer = $q.defer();
            $http({
                method: "GET",
                url: "api/location" + id + "/"
            }).success(function (data, status, headers, config) {
                defer.resolve(data);
            }).error(function (data, status, headers, config) {
                defer.reject(status);
            });
            return defer.promise;
        },
        createLocation: function (data) {
            var defer = $q.defer();
            console.log(angular.toJson(data, true));
            $http({
                method: "POST",
                url: "api/location/",
                data: angular.toJson(data, true)
            }).success(function (data, status, headers, config) {
                defer.resolve(data);
            }).error(function (data, status, headers, config) {
                defer.reject(status);
            });
            return defer.promise;
        },
        updateLocation: function (id, data) {
            var defer = $q.defer();
            $http({
                method: "PUT",
                url: "api/location/" + id + "/",
                data: data
            }).success(function (data, status, headers, config) {
                defer.resolve(status, data);
            }).error(function (data, status, headers, config) {
                defer.reject(status);
            });
            return defer.promise;
        },
        deleteLocation: function (id) {
            var defer = $q.defer();
            $http({
                method: "DELETE",
                url: "api/location/" + id + "/"
            }).success(function (data, status, headers, config) {
                defer.resolve(data);
            }).error(function (data, status, headers, config) {
                defer.reject(status);
            });
            return defer.promise;
        }

    };
}]);