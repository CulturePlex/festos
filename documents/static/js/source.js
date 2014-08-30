(function($) {
    $(document).ready(function($) {
        $('input:radio[name="source"]').change(function(){
            if ($(this).is(':checked') && $(this).val() == 'local') {
                $("#id_docfile").parent().parent().show()
                $(".dropbox-dropin-btn").parent().parent().hide()
            }
            if ($(this).is(':checked') && $(this).val() == 'dropbox') {
                $("#id_docfile").parent().parent().hide()
                $(".dropbox-dropin-btn").parent().parent().show()
            }
        });
        if ($('input:radio[name="source"][value="local"]').is(":checked"))
            $(".dropbox-dropin-btn").parent().parent().hide()
        else
            $("#id_docfile").parent().parent().hide()
    });
})(jQuery);
