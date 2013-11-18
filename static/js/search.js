$(document).ready(function(){
  $("a.summary").ellipsis();
  $(window).resize(
    function(){
      $("a.summary").ellipsis();
    }
  );
});
