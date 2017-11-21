/*global $*/
(function(){

  $('[data-toggle="tooltip"]').tooltip()

  // console.log('hit');
  window.jsCopy = function(id){
    // console.log(id)
    var copyText = document.getElementById(id);
    copyText.focus();
    copyText.select();
    document.execCommand("copy");
    $.notify('Link Copied', "success");
  };
})($);