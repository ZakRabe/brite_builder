/*global $*/
(function(){

  $('[data-toggle="tooltip"]').tooltip()

  console.log('hit');
  window.jsCopy = function(id){
    var copyText = document.getElementById(id);
    copyText.select();
    document.execCommand("Copy");
    $.notify('Link Copied', "success");
  }
})($);