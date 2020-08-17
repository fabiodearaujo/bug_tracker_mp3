
// Materialize initialization JQuery code 
$(document).ready(function(){
    $(".sidenav").sidenav({edge: "right"});
    $('input#user_name, input#user_pass').characterCounter();
});