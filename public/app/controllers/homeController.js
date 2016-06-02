app.controller("HomeController", [
    "$scope",
    "$location",
    "$log",
    function ($scope, $location, $log) {
        'use strict';


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