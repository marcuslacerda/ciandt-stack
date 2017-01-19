'use strict';

app.config(['$httpProvider', function($httpProvider) {
  $httpProvider.interceptors.push(['$q', '$location', '$rootScope', '$injector', function($q, $location, $rootScope, $injector) {

    return {
      responseError: function(response) {
        console.log('STATUS => ' + response.status)
        console.log('Attempt URL ' + $location.path())
        if (response.status === 401 || response.status === 403) {
          var $auth = $injector.get('$auth')
          $auth.logout()
          $location.path('/login')
        }
        return $q.reject(response);
      }
    };

  }]);

}]);
