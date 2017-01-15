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

    $scope.stack = data[0];
    achieve = $scope.stack.index
    console.log(achieve)
    $scope.memoryChartData = [ {key: 'achieve', y: achieve}, { key: 'necessity', y: 1-achieve} ];

  });

  // tkci graph
  var vm = this;

  // TODO: move data to the service


  $scope.chartOptions = {
      chart: {
          type: 'pieChart',
          height: 210,
          donut: true,
          pie: {
              startAngle: function (d) { return d.startAngle/2 -Math.PI/2 },
              endAngle: function (d) { return d.endAngle/2 -Math.PI/2 }
          },
          x: function (d) { return d.key; },
          y: function (d) { return d.y; },
          valueFormat: (d3.format(",.0%")),
          // color: ['#E53935', '#BDBDBD'],
          color: ['#00897B', '#BDBDBD'],
          showLabels: false,
          showLegend: true,
          tooltips: false,
          title: 'TKCI',
      }
  };


}]);
