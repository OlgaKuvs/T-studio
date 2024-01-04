let countySelected = $('#id_profile_county').val();
if(!countySelected) {
    $('#id_profile_county').css('color', '#636c72');
};
$('#id_profile_county').change(function() {
    countySelected = $(this).val();
    if(!countySelected) {
        $(this).css('color', '#636c72');
    } else {
        $(this).css('color', '#292f36');
    }
});


