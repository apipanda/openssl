app.config(["$routeProvider", function ($routeProvider) {
    "use strict";
    $routeProvider.when('/', {
        controller: 'HomeController',
        controllerAs: 'vm',
        templateUrl: '../app/views/map.html',
        resolve: {}
    })
        .otherwise({redirectTo: '/'});
}])
    .config(['$httpProvider', function ($httpProvider) {
        "use strict";
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    }])
    .config(['$interpolateProvider', function ($interpolateProvider) {
        "use strict";
        $interpolateProvider.startSymbol('{$');
        $interpolateProvider.endSymbol('$}');
    }]);