app.config(["$routeProvider", '$locationProvider', function ($routeProvider, $locationProvider) {
    "use strict";
    $locationProvider.html5Mode(true);
    $routeProvider.caseInsensitiveMatch = true;

    $routeProvider.when('/start', {
        controller: 'HomeController',
        controllerAs: 'vm',
        templateUrl: '/home'
    })
        .when('/verify', {
            controller: 'VerifyController',
            controllerAs: 'vm',
            templateUrl: '/verification'
        })
        .when('/login', {
            controller: 'LoginController',
            controllerAs: 'vm',
            templateUrl: '/signin'
        })
        .when('/signup', {
            controller: 'RegisterController',
            controllerAs: 'vm',
            templateUrl: '/join'
        })
        .when('/recover', {
            controller: 'ResetController',
            controllerAs: 'vm',
            templateUrl: '/reset'
        })
        .when('/guide', {
            controller: 'GuideController',
            controllerAs: 'vm',
            templateUrl: '/guides'
        })
        .when('/blog', {
            controller: 'BlogController',
            controllerAs: 'vm',
            templateUrl: '/post/'
        })
        .when('/blog/:path*', {
            controller: 'PostController',
            controllerAs: 'vm',
            templateUrl: function (params) {
                // body...
                return '/post/' + params.path;
            }
        })

        .whenAuthenticated('/dashboard', {
            controller: 'DashController',
            controllerAs: 'vm',
            templateUrl: '/dashy'
        })
        .whenAuthenticated('/domains', {
            controller: 'DomainController',
            controllerAs: 'vm',
            templateUrl: '/domain'
        })
        .whenAuthenticated('/bulletin', {
            controller: 'MessageController',
            controllerAs: 'vm',
            templateUrl: '/notification'
        })
        .whenAuthenticated('/logs', {
            controller: 'LogController',
            controllerAs: 'vm',
            templateUrl: '/stats'
        })
        .whenAuthenticated('/domain/edit', {
            controller: 'EditController',
            controllerAs: 'vm',
            templateUrl: '/edit'
        })
        .whenAuthenticated('/profile', {
            controller: 'ProfileController',
            controllerAs: 'vm',
            templateUrl: '/user'
        })

        .otherwise({redirectTo: '/start'});
}])
    .config(['$httpProvider', function ($httpProvider) {
        "use strict";
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    }])
    .config(['$interpolateProvider', function ($interpolateProvider) {
        "use strict";
        $interpolateProvider.startSymbol('{$');
        $interpolateProvider.endSymbol('$}');
    }])
    .config(['cfpLoadingBarProvider', function(cfpLoadingBarProvider) {
        cfpLoadingBarProvider.includeSpinner = false;
      }])
    .config(['$localStorageProvider', function ($localStorageProvider) {
        "use strict";
        $localStorageProvider.setKeyPrefix('pandassl-');
    }]);

