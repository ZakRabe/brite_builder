/*global $*/
(function(){

var app = angular.module('brite_builder', []);

var clean = function(value){
  return value.toLowerCase().replace(" ",'-');
}

app.controller('loadoutCtrl', function ($scope) {
  
  $scope.testModel ={
    id:1,
    title: "Frog Frenzy",
    description:"Toxin Blades bonus damage is increased by 1 and it increases the attack speed of your next 6 Blade Flurry swings",
    spell:{
      title: "Toxin Blades",
      button: "R",
      champ:{
        title: "Croak"  ,
        subtitle: "The Ranid Assassin",
      },
    },
    type:{
      title: "Offense",
    },   
  };
  $scope.loadout = {
    build_hash: null,
    talent_0: $scope.testModel,
    talent_1: null,
    talent_2: null,
    talent_3: null,
    talent_4: null,
  };
  $scope.addTalent = function(talent){
    for (var i = 0; i < 5; i++) {
      if ($scope.loadout['talent_' + i].id == talent.id) {
        console.log("already exists in the build");
        return false;
      }
    }
    for (var i = 0; i < 5; i++) {
      if (!$scope.loadout['talent_' + i]) {
        $scope.loadout['talent_' + i] = talent;
        return true;
      }
    }
    console.log('build is full');
    return false;
  };
  $scope.removeTalent = function(talent){
    for (var i = 0; i < 5; i++) {
      if ($scope.loadout['talent_' + i].id == talent.id) {
        $scope.loadout['talent_' + i] = null;
        // todo: success reporting
        return true;
      }
    }
    // todo: error reporting
    console.log('talent not found in build');
    return false;
  };
  
});

app.controller('champTalentPoolCtrl', function ($scope, $http, $attrs) {
  
  $scope.testModel ={
    id:1,
    title: "Frog Frenzy",
    description:"Toxin Blades bonus damage is increased by 1 and it increases the attack speed of your next 6 Blade Flurry swings",
    spell:{
      title: "Toxin Blades",
      button: "R",
      champ:{
        title: "Croak"  ,
        subtitle: "The Ranid Assassin",
      },
    },
    type:{
      title: "Offense",
    },   
  };
  $scope.talentPool = [];
  var loadTalents = function(returned){
    $scope.talentPool = returned.data;
  };
  $http.get('talents/'+ clean($attrs.champ)).then(loadTalents);
  
});


app.directive('talent', ["$compile", '$http', '$templateCache', '$parse', 
function($compile, $http, $templateCache, $parse){
  return {
    templateUrl: '/talents/render/',
    scope:{
      model: '=',
    },
    link: function(scope){
      scope.init = !(scope.model==null);
      scope.clean = clean;
      scope.add_or_remove = function(talent){
        if (scope.$parent.loadout) {
          scope.$parent.removeTalent(talent);
        }else{
          scope.$parent.addTalent(talent);
        }
      }
    }
  };
}]);
/*
  

*/
})($);