app.config(["$routeProvider", '$locationProvider', function ($routeProvider, $locationProvider) {
    "use strict";
    $locationProvider.html5Mode(true);

    $routeProvider.when('/start', {
        controller: 'HomeController',
        controllerAs: 'vm',
        templateUrl: '/home'
    })
        .when('/verify', {
            controller: 'verifyController',
            controllerAs: 'vm',
            templateUrl: '/verification'
        })
        .when('/login', {
            controller: 'LoginController',
            controllerAs: 'vm',
            templateUrl: '/signin'
        })
        // .when('/signup', {
        //     controller: 'RegisterController',
        //     controllerAs: 'vm',
        //     templateUrl: '../register/'
        // })
        .when('/recover', {
            controller: 'ResetController',
            controllerAs: 'vm',
            templateUrl: '/reset'
        })

        // .whenAuthenticated('/switcher', {
        //     controller: 'SwitchController',
        //     controllerAs: 'vm',
        //     templateUrl: '../switcher/'
        // })

        // .whenAuthenticated('/dashboard', {
        //     controller: 'DashController',
        //     controllerAs: 'vm',
        //     templateUrl: '../dashboard/'
        // })

        // .whenAuthenticated('/dashboard/hubs', {
        //     controller: 'HubController',
        //     controllerAs: 'vm',
        //     templateUrl: '../hub/'
        // })

        // .whenAuthenticated('/dashboard/orgs', {
        //     controller: 'OrgController',
        //     controllerAs: 'vm',
        //     templateUrl: '../orgs/'
        // })

        // .whenAuthenticated('/dashboard/workspaces', {
        //     controller: 'WorkspaceController',
        //     controllerAs: 'vm',
        //     templateUrl: '../workspaces/'
        // })

        // .whenAuthenticated('/dashboard/plugins', {
        //     controller: 'PluginController',
        //     controllerAs: 'vm',
        //     templateUrl: '../plugins/'
        // })

        // .whenAuthenticated('/profile', {
        //     controller: 'ProfileController',
        //     controllerAs: 'vm',
        //     templateUrl: '../profile/'
        // })

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
        cfpLoadingBarProvider.includeSpinner = true;
      }])
    .config(['$localStorageProvider', function ($localStorageProvider) {
        "use strict";
        $localStorageProvider.setKeyPrefix('pandassl');
    }]);

