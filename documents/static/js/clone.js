$(document).ready(function() {
    $(".non-clonable-field #id_all_fields").live("click", function(ev) {
        $(".clonable-field input").prop("checked", $(this).is(":checked"));
    })
    
    $(".clonable-field input").live("click", function(ev) {
        if (!$(this).is(":checked"))
           $(".non-clonable-field #id_all_fields").prop("checked", false);
        if ($(".clonable-field input").not(":checked").length == 0)
           $(".non-clonable-field #id_all_fields").prop("checked", true);
    })
})




