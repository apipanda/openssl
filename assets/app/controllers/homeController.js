app.controller("HomeController", [
    "$scope",
    "$location",
    "$log",
    "uiGmapGoogleMapApi",
    "LocationService",
    "FusiontableService",
    function ($scope, $location, $log, uiGmapGoogleMapApi, LocationService, FusiontableService) {
        'use strict';

        $scope.map = {
            center: {
                latitude: 45,
                longitude: -73
            },
            zoom: 10,
            pan: true,
            options: {
                disableDefaultUI: true
            },
            events: {
                click: getPlace
            }
        };

        $scope.fetchall = function () {
            FusiontableService.listAll()
                .then(function (result) {
                    $scope.locations = result.rows
                }, function (err) {
                    $log.error(err);
                });
        }

        $scope.saveLocation = function (payload) {
            LocationService.createLocation(payload)
                .then(function (status, data) {
                    FusiontableService.createRow(payload)
                        .then(function (result) {
                            console.log(result);
                            $scope.fetchall();
                        }, function (error) {
                            $log.error(error);
                        })
                }, function (error) {
                    $log.error(error);
                })
        }

        // analyze the map click event
        function getPlace (map, e, point) {
            var address, place_id, payload, geocoder;

            var latLng = point[0].latLng;
            var lat = latLng.lat();
            var lng = latLng.lng();
            $scope.center = {
                longitude: lng,
                latitude: lat
            };

            geocoder = new google.maps.Geocoder();
            geocoder.geocode({location: latLng}, function (result, status) {
                 if (status == google.maps.GeocoderStatus.OK) {

                    // result type can either be a string instance or an array of strings
                    if (result.types !== 'natural_feature' || result.types.indexOf('natural_feature') >= 0)  {
                        address = result[0].formatted_address;
                        place_id = result[0].place_id;
                        payload = {
                            address: address,
                            longitude: lng,
                            latitude: lat,
                            latlng: latLng,
                            place_id: place_id,
                            created_on: Date()
                        };
                        $scope.saveLocation(payload);
                    }
                }
            });
            handleAuthClick();
        }

        $log.debug("Home Controller Initialized");
    }]);
var clientId = 'codesses-1131';
var apiKey = 'AIzaSyAJE9zPetSqwHzkvm9VkIqNwedvUWh92JM';
var scopes = ['https://www.googleapis.com/auth/fusiontables']

function handleClientLoad() {
  gapi.client.setApiKey(apiKey);
  window.setTimeout(checkAuth,1);
}

function checkAuth() {
  gapi.auth.authorize({client_id: clientId, scope: scopes, immediate: true}, handleAuthResult);
}

function handleAuthResult(authResult) {
  var authorizeButton = document.getElementById('authorize-button');
  if (authResult && !authResult.error) {
    authorizeButton.style.visibility = 'hidden';
    console.log(authResult);
  } else {
    authorizeButton.style.visibility = '';
    authorizeButton.onclick = handleAuthClick;
  }
}

function handleAuthClick() {
  gapi.auth.authorize({client_id: clientId, scope: scopes, immediate: false}, handleAuthResult);
  return false;
}