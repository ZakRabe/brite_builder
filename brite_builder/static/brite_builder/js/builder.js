/*global $*/
/*global angular*/
(function(){
var clean = function(value){
  if (value) {
    return value.toLowerCase().replace(/ /g,'-').replace(/'/g,'').replace(/"/g,'');
  }
  return '';
};

var csrfToken = window.csrfToken = function(){
  return $("[name=csrfmiddlewaretoken]").val();
};

var app = angular.module('brite_builder', ['ngSanitize', 'ngclipboard']).config(function($httpProvider) {
  $httpProvider.defaults.headers.post['X-CSRFToken'] = csrfToken();
});


app.controller('loadoutCtrl', function ($scope, $http, $timeout) {
  $scope.copy_class = "info";
  $scope.copy_url = function(){
    $scope.copy_class = "success";
    $.notify('Link Copied', "success");
  };
  $scope.build_hash = function(){
    var talent_ids = [];
    for (var i = 0; i < 5; i++) {
      var talent = $scope.loadout['talent_'+i];
      if (talent) {
        var talent_id = talent.id;
        talent_ids.push(talent_id);
      }
    }
    talent_ids.sort();
    var output = '';
    for (var i = 0; i < talent_ids.length; i++) {
      var id = talent_ids[i];
      output += id;
      if (i < talent_ids.length-1) {
        output+= ",";
      }
    }
    // remove trailing comma just in case we have incomplete build
    if (output.charAt(output.length-1) == ",") {
      output=output.substring(0, output.length-1);
    }
    $scope.copy_class = 'info';
    var url = "https://" + window.location.hostname + "/" + window.location.pathname.split('/')[1] + "/" + output;
    if (output.length) {
      url += "/";
    }

    if ($scope.build.id) {
      url += $scope.build.id + '/';
    }
    // console.log(url);
    window.history.pushState('', 'Counter.GG', url);
    $scope.build_url = url;
  };
  $scope.is_empty = function(talent){
    // console.log(talent)
    if (!talent) {
      // console.log('hit');
      return 'is-empty';
    }
    return '';
  };
  $scope.toggleTalent = function(talent){
    if (talent.selected) {
      return $scope.removeTalent(talent);
    }else{
      return $scope.addTalent(talent);
    }
  };
  $scope.removeTalent = function(talent){
    var loadout = $scope.loadout;
    for (var i = 0; i < 5; i++) {
      if ((loadout['talent_'+i] && talent) && loadout['talent_'+i].id == talent.id) {
        loadout['talent_'+i] = null;
        $scope.loadout = loadout;
        var champPoolTalent = $('[ng-controller="champTalentPoolCtrl"] [data-talent-id='+talent.id+']');
        var talent_scope = angular.element(champPoolTalent).scope();
        talent_scope.model.selected = false;
        $scope.build_hash();
        return false;
      }
    }
    console.log('Talent not found in loadout.');
    return false;
  };
  $scope.addTalent = function(talent){
    var loadout = $scope.loadout;

    for (var i = 0; i < 5; i++) {
      // console.log(talent.id);
      if (loadout['talent_'+i] && loadout['talent_'+i].id == talent.id) {
        console.log("Loadout already contains this talent");
        return true;
      }
    }
    var spell_id = talent.spell.id;
    // count current loadout spells. no more than 2 for each spell
    var spellCount = 0;
    for (var i = 0; i < 5; i++) {
      if (loadout['talent_'+i]) {
        if (spell_id == loadout['talent_'+i].spell.id && !talent.no_limit ) {
          spellCount++;
        }
      }
    }
    if (spellCount >=2) {
      $.notify('Cant have more than 2 talents active per spell', "error");
      return false;
    }
    for (var i = 0; i < 5; i++) {
      if (!loadout['talent_'+i]) {
        loadout['talent_'+i] = talent;
        $scope.loadout = loadout;
        $scope.build_hash();
        return true;
      }
    }
    return $.notify('Loadout is full.', "error");
  };
  var saveBuildSuccess = function(returned){
    console.log(returned);
    var data = returned.data;
    if (data.errors) {
      $scope.errors = data.errors.valid;
      for (var i = 0; i < $scope.errors.length; i++) {
        $.notify($scope.errors[i], "error");
      }
    }else{
      $scope.loadout = data.success.loadout;
      $scope.build = data.success.build;
      $scope.build_hash();
      $.notify('Saved successfully', "success");
    }
  };
  $scope.saveBuild = function(){
    $http.post('/builds/', {'build':$scope.build, 'loadout':$scope.loadout}).then(saveBuildSuccess);
  };

  var blank_loadout = {
    id: null,
    build_hash: null,
    talent_0: null,
    talent_1: null,
    talent_2: null,
    talent_3: null,
    talent_4: null,
  };
  var blank_build =  {
    id: null,
    title: 'New Loadout',
    description: '',
    loadout_id: null,
  };
  $scope.copyBuild = function(){
    $scope.build = blank_build;
    $scope.build_hash()
  };

  $scope.loadout = blank_loadout;
  $scope.build = blank_build;
  if (window.loadout) {
    $scope.loadout.id = window.loadout.id;
    $scope.loadout.build_hash = window.loadout.build_hash;
    var talent_ids = [];
    for (var i = 0; i < 5; i++) {
      var talent = window.loadout['talent_' + i];
      if (!talent) {
        if (window.loadout[i]) {
          talent_ids.push(window.loadout[i]);
        }
      }else{
        talent_ids.push(talent.id);
      }
    }
    var count = 0;
    var tryClick = function(){
      if(count < 50){
        for (var i = 0; i < talent_ids.length; i++) {
          var id = talent_ids[i];
          var el = $("div[ng-controller=champTalentPoolCtrl] div[data-talent-id="+id+"]");
          if (el.length) {
            // console.log(id);
            var is_talent_0 = Boolean($scope.loadout.talent_0 && $scope.loadout.talent_0.id == id);
            var is_talent_1 = Boolean($scope.loadout.talent_1 && $scope.loadout.talent_1.id == id);
            var is_talent_2 = Boolean($scope.loadout.talent_2 && $scope.loadout.talent_2.id == id);
            var is_talent_3 = Boolean($scope.loadout.talent_3 && $scope.loadout.talent_3.id == id);
            var is_talent_4 = Boolean($scope.loadout.talent_4 && $scope.loadout.talent_4.id == id);
            /*console.log(is_talent_0);
            console.log(is_talent_1);
            console.log(is_talent_2);
            console.log(is_talent_3);
            console.log(is_talent_4);*/
            if (
              !is_talent_0 && !is_talent_1 && !is_talent_2 && !is_talent_3 && !is_talent_4
            ) {
              el.click();
            }else{
              continue;
            }
          }else{
            count++;
            $timeout(tryClick, 100);
          }
        }
      }
     };
    $timeout(tryClick,100);
  }
  if (window.build) {
    $scope.build = window.build;
  }
  $scope.build_hash();
});

app.controller('champTalentPoolCtrl', function ($scope, $http, $attrs) {

  $scope.talentPool = [];
  var loadTalents = function(returned){
    $scope.talentPool = returned.data;
  };
  $http.get('/talents/'+ clean($attrs.champ)).then(loadTalents);




});


app.directive('talent', ["$compile", '$http', '$templateCache', '$parse',
function($compile, $http, $templateCache, $parse){
  return {
    templateUrl: '/talents/render/',
    scope:{
      model: '=',
    },
    link: function(scope, attrs, el){
      scope.init = !(scope.model==null);
      scope.clean = clean;
    }
  };
}]);


})($, angular);