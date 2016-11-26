String.prototype.format = function (obj) {
    // Not optimal, but clean and serves the desired purpose
    return this.replace(/{([^{}]*)}/g,
        function (a, b) {
            var r = obj[b];
            return typeof r === 'string' || typeof r === 'number' || 'object' ? r : a;
        }
    );
};

app.service(
    'FusiontableService',
    [
        "$http",
        "$q",
        "FUSION_TABLE_ID",
        "GOOGLE_API_KEY",
        "GOOGLE_API_AUTH",
        "FUSION_TABLE_URL",
        function ($http, $q, FUSION_TABLE_ID, GOOGLE_API_KEY, GOOGLE_API_AUTH, FUSION_TABLE_URL) {
            'use strict';
            var url = FUSION_TABLE_URL + FUSION_TABLE_ID + '/?key' + GOOGLE_API_KEY;
            var queryUrl = FUSION_TABLE_URL + 'query?key=' + GOOGLE_API_KEY + '&sql=';
            var headers = {
                "Authorization": "Basic {0}".format([GOOGLE_API_AUTH])
            }
            return {
                listAll: function () {
                    var query = "SELECT * FROM " + FUSION_TABLE_ID
                    queryUrl += query;
                    console.log(queryUrl);
                    var defer = $q.defer();
                    $http({
                        method: "GET",
                        url: queryUrl
                    }).success(function (data, status, headers, config) {
                        defer.resolve(data);
                    }).error(function (data, status, headers, config) {
                        defer.reject(status);
                    });
                    return defer.promise;
                },
                getFusiontable: function (id) {
                    var defer = $q.defer();
                    $http({
                        method: "GET",
                        url: queryUrl + id + "/"
                    }).success(function (data, status, headers, config) {
                        defer.resolve(data);
                    }).error(function (data, status, headers, config) {
                        defer.reject(status);
                    });
                    return defer.promise;
                },
                createRow: function (data) {
                    console.log(data);
                    var query = "INSERT INTO " + FUSION_TABLE_ID +  "(address, latitude, longitude, created_on, place_id) VALUES ('{address}', '{latitude}', '{longitude}', '{created_on}', '{place_id}')".format(data);
                    queryUrl += query;
                    console.log(queryUrl);
                    var defer = $q.defer();
                    $http({
                        method: "POST",
                        url: queryUrl,
                        headers: headers
                    }).success(function (data, status, headers, config) {
                        defer.resolve(data);
                    }).error(function (data, status, headers, config) {
                        defer.reject(status);
                    });
                    return defer.promise;
                },
                updateFusiontable: function (id, data) {
                    var defer = $q.defer();
                    $http({
                        method: "PUT",
                        url: queryUrl + id + "/",
                        data: data
                    }).success(function (data, status, headers, config) {
                        defer.resolve(data);
                    }).error(function (data, status, headers, config) {
                        defer.reject(status);
                    });
                    return defer.promise;
                },
                deleteFusiontable: function (id) {
                    var defer = $q.defer();
                    $http({
                        method: "DELETE",
                        url: queryUrl + id + "/"
                    }).success(function (data, status, headers, config) {
                        defer.resolve(data);
                    }).error(function (data, status, headers, config) {
                        defer.reject(status);
                    });
                    return defer.promise;
                }

            };
}]);