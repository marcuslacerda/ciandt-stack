app.controller('StackController', ['$scope', '$stateParams', '$mdDialog', '$resource', '$timeout', '$mdSidenav', '$log', 'Analytics', function($scope, $stateParams, $mdDialog, $resource, $timeout, $mdSidenav, $log, Analytics){

  $scope.key = $stateParams.key

  var StackAPI = $resource('api/stacks/:action',
      { q : '@q' },
      {
        list : { method : 'GET', isArray: true },
        search : { method : 'GET', params : {action : '_search'}, isArray: true }
      }
  );


  Analytics.trackEvent('action', 'view', $scope.key);

  q = 'key:' + $scope.key

  console.log('loading stack ' + q)
  StackAPI.search({ q: q }, function(data){
    console.log('sucesso')
    console.log(data[0])
    $scope.stack = data[0];
  });

}]);
