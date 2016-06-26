// when $routeProvider.whenAuthenticated() is called, the path is stored in this list
// to be used by authRequired() in the services below
var securedRoutes = [];

/**
* Adds a special `whenAuthenticated` method onto $routeProvider. This special method,
* when called, waits for auth status to be resolved asynchronously, and then fails/redirects
* if the user is not properly authenticated.
*
* The promise either resolves to the authenticated user object and makes it available to
* dependency injection (see AuthCtrl), or rejects the promise if user is not logged in,
* forcing a redirect to the /login page
*/
app.config(['$routeProvider', function ($routeProvider) {
  // credits for this idea: https://groups.google.com/forum/#!msg/angular/dPr9BpIZID0/MgWVluo_Tg8J
  // unfortunately, a decorator cannot be use here because they are not applied until after
  // the .config calls resolve, so they can't be used during route configuration, so we have
  // to hack it directly onto the $routeProvider object
  $routeProvider.whenAuthenticated = function (path, route) {
    securedRoutes.push(path); // store all secured routes for use with authRequired() below
    route.resolve = route.resolve || {};
    route.resolve.user = ['Auth', function (Auth) {
      return Auth.$requireAuth();
    }];

    $routeProvider.when(path, route);
    return this;
  }
}])

.config(['$httpProvider', 'API_USER', 'API_KEY', function($httpProvider, API_USER, API_KEY) {
  $httpProvider.defaults.headers.common['Authorization'] = "ApiKey " + API_USER + ":" + API_KEY;
}])

/**
* Apply some route security. Any route's resolve method can reject the promise with
* { authRequired: true } to force a redirect. This method enforces that and also watches
* for changes in auth status which might require us to navigate away from a path
* that we can no longer view.
*/
.run(['$rootScope', '$location', 'Auth', 'loginRedirectPath', '$localStorage', '$sessionStorage',
  function ($rootScope, $location, Auth, loginRedirectPath, $localStorage, $sessionStorage) {
    // watch for login status changes and redirect if appropriate
    // Auth.$onAuth(check);
    $rootScope.user = $localStorage.user;
    $rootScope.logout = Auth.$logout;
    // some of our routes may reject resolve promises with the special {authRequired: true} error
    // this redirects to the login page whenever that is encountered
    $rootScope.$on("$routeChangeError", function (e, next, prev, err) {
      if (err === "AUTH_REQUIRED") {
        $location.path(loginRedirectPath);
      }
    });

    $rootScope.$on("$routeChangeStart", function(e, next, current){

      if (!!next) {
        if (next.originalPath.toLowerCase() === '/login' || next.originalPath.toLowerCase() === '/signup') {
          if (!!$sessionStorage.auth || !!$localStorage.auth) {
            $location.path('/dashboard');
          };
        };
      } else {
        if (current.originalPath.toLowerCase() === '/login' || current.originalPath.toLowerCase() === '/signup') {
          if (!!$sessionStorage.auth || !!$localStorage.auth) {
            $location.path('/dashboard');
          };
        };
      }
    });

    function check(user) {
      if (!$localStorage.user && authRequired($location.path())) {
        $location.path(loginRedirectPath);
      }
    }

    function authRequired(path) {
      console.log('authRequired?', path, securedRoutes.indexOf(path)); //debug
      return securedRoutes.indexOf(path) !== -1;
    }
  }
]);

