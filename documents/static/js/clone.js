$(document).ready(function() {
    $(".non-clonable-field #id_all_fields").live("click", function(ev) {
        $(".clonable-field input").prop("checked", $(this).is(":checked"));
    })
    
    $(".clonable-field input").live("click", function(ev) {
        if ($(this).not(":checked"))
           $(".non-clonable-field #id_all_fields").prop("checked", false);
    })
})




