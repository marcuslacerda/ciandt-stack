app.controller('StacksController', ['$scope', '$mdDialog', '$resource', '$timeout', '$mdSidenav', '$log', 'Analytics', function($scope, $mdDialog, $resource, $timeout, $mdSidenav, $log, Analytics){

  $scope.input = ''

  var StackAPI = $resource('api/stacks/:action',
      { q : '@q' },
      {
        list : { method : 'GET', isArray: true },
        search : { method : 'GET', params : {action : '_search'}, isArray: true }
      }
  );

  $scope.search = function() {
    Analytics.trackEvent('action', 'search', $scope.input);

    q = $scope.input
    if (q == '' || q == null) {
      q = "*"
    }

    StackAPI.search({ q: q }, function(data){
      $scope.projects = data;
    });
  };

  StackAPI.list(function(data){
    $scope.projects = data;
  });

  // ----------------------------
  // -- Team view. Modal per stack id
  // ----------------------------
  $scope.showTeam = function(ev, id) {
    Analytics.trackEvent('action', 'showTeam', id);
    // GET team for stack id
    url = 'api/stacks/team/' + id
    var TeamApi = $resource(url);
    TeamApi.query(function(data){
      $mdDialog.show({
        controller: DialogController,
        templateUrl: 'partials/dialog-team.html',
        targetEvent: ev,
        locals : {team : data},
        clickOutsideToClose: true,
        escapeToClose: true
      })
      .then(function(answer) {
        $scope.alert = 'You said the information was "' + answer + '".';
      }, function() {
        $scope.alert = 'You cancelled the dialog.';
      });
    });
  };


  $scope.startSearch = function() {
    $scope.showSearch = true
    $timeout(function () {
            document.getElementById('search_input').focus();
    }, 10);
  }

$scope.finishSearch = function() {
    // hide input
    $scope.showSearch = false

    // clear input value
    $scope.input = ''

    // list all stacks
    StackAPI.list(function(data){
      $scope.projects = data;
    });
  }


  // ----------------------------
  // -- Key press feature ng-keyup function
  // ----------------------------
  $scope.keyPress = function(event){
    console.log(event.keyCode + ' - ' + event.altKey);

    // if keyCode = ENTER (#13)
    if ($scope.showSearch) {
      if (event.keyCode == 13) {
        $scope.search()
      }
      // if keyCode = ESC (#27)
      if (event.keyCode == 27) {
        $scope.finishSearch()
      }
    }
  };

  // ----------------------------
  // -- Left NavBard
  // ----------------------------
  var TrendsAPI = $resource('api/trends/:action',
      { q : '@q' },
      {
        owners : { method : 'GET', params : {action : 'owners'}, isArray: true },
        techs : { method : 'GET', params : {action : 'technologies'}, isArray: true }
      }
  );

  TrendsAPI.owners(function(data){
    console.log('list owners')
    $scope.owners = data;
  });

  // TrendsAPI.techs(function(data){
  //   $scope.techs = data;
  // });

  $scope.toggleLeft = function () {
    $mdSidenav('left').toggle()
      .then(function () {
        $log.debug("close LEFT is done");
      });
  }

  $scope.close = function () {
    $mdSidenav('left').close()
      .then(function () {
        $log.debug("close LEFT is done");
      });
  };

  //$scope.toggleLeft();

  $scope.ownersSelected = [];
  $scope.techsSelected = [];
  /*
   * Function called when checkbox is selected to filter
   * stack cards. List ownersSelected and techsSelected
   * will be used
   */
  $scope.toggle = function (item, list) {
    $log.debug('toggle')
    var idx = list.indexOf(item);
    if (idx > -1) {
      list.splice(idx, 1);
    }
    else {
      list.push(item);
    }

    // -- trigger search by owners and techs
    // $log.debug(buildQueryParam('owner', list))
    queryOwners = buildQueryParam('owner', $scope.ownersSelected)
    queryTechs = buildQueryParam('stack.technologyName', $scope.techsSelected)
    param =  queryOwners + ' AND ' + queryTechs
    $log.debug('query parma: ' + param)
    $log.debug("changeItem - searching");

    Analytics.trackEvent('action', 'toggle', param);

    StackAPI.search({ q: param }, function(data){
      $scope.projects = data;
    });

  };

  function buildQueryParam(field, list) {
    if (list.length > 0) {
      var query = field + ':(';
      var first = list[0];
      query = query + first.name;
      for (var i = 1; i < list.length; i++) {
        item = list[i];
        query = query + ' OR ' + item.name;
      }
      query = query + ')';
      return query;
    } else {
      return '*';
    }
  }


  // ----------------------------
  // -- Favorite Actions
  // ----------------------------
  $scope.likeCount = 2

  $scope.like = function(item) {
    item.like_count += 1
    console.log('TODO: async call to update like action' + item.key)
  }

}]);

function DialogController($scope, $mdDialog, team) {
  $scope.team =  team

  $scope.hide = function() {
    $mdDialog.hide();
  };
  $scope.cancel = function() {
    $mdDialog.cancel();
  };
  $scope.answer = function(answer) {
    $mdDialog.hide(answer);
  };
};
