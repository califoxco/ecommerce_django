
$( document ).ready(function() {
    $('.billing').hide();
    $( "#same-address" ).change(function() {
    if ($("#same-address").is(":checked")){
        $('.billing').hide();
    }
    else {
        $('.billing').show();
    }
    });
});