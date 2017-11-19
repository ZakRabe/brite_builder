/*global $*/
/*global angular*/
(function(){
var clean = function(value){
  if (value) {
    return value.toLowerCase().replace(/ /g,'-').replace(/'/g,'').replace(/"/g,'');
  }
  return '';
};

var app = angular.module('brite_builder', ['ngSanitize']);


app.controller('loadoutCtrl', function ($scope) {
  // $scope.testModel ={
  //   id:1,
  //   title: "Frog Frenzy",
  //   description:"Toxin Blades bonus damage is increased by 1 and it increases the attack speed of your next 6 Blade Flurry swings",
  //   spell:{
  //     title: "Toxin Blades",
  //     button: "R",
  //     champ:{
  //       title: "Croak"  ,
  //       subtitle: "The Ranid Assassin",
  //     },
  //   },
  //   type:{
  //     title: "Offense",
  //   },
  // };
  $scope.loadout = {
    id: null,
    build_hash: null,
    talent_0: null,
    talent_1: null,
    talent_2: null,
    talent_3: null,
    talent_4: null,
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
        return true;
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
        if (spell_id == loadout['talent_'+i].spell.id) {
          spellCount++;
        }
      }
    }
    if (spellCount >=2) {
      console.log('Cant have more than 2 talents active per spell');
      return false;
    }
    for (var i = 0; i < 5; i++) {
      if (!loadout['talent_'+i]) {
        loadout['talent_'+i] = talent;
        $scope.loadout = loadout;
        return true;
      }
    }
    return console.log("Loadout is full.");
  };



});

app.controller('champTalentPoolCtrl', function ($scope, $http, $attrs) {

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
    }
  };
}]);


})($, angular);