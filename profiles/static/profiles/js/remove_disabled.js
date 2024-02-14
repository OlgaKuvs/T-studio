//  Remove disabled attribute from form fields
$('#add-address-form').submit(function(){
    $('#add-address-form :disabled').removeAttr('disabled');
    });

$('#edit-address-form').submit(function(){
    $('#edit-address-form :disabled').removeAttr('disabled');
    });