
// Materialize initialization JQuery code 
$(document).ready(function(){
    $(".sidenav").sidenav({edge: "right"});
    $('select').formSelect();
    $('input#user_name, input#user_pass').characterCounter();
});