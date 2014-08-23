(function($) {
    $(document).ready(function($) {
        $("#id_applied").prop('disabled', true);
        if ($('#id_region').val()) {
            $("input[name='_save']").hide();
            $("input[name='_continue']").hide();
            $("input[name='_addanother']").hide();
            $("#id_region").prop('disabled', true);
            $("#id_raw").prop('disabled', true);
            if (!$("#id_applied").prop('checked')) {
                $(".submit-row").append('<input type="submit" value="Применить!" class="default" name="_apply"/>');
                $("input[name='_apply']").click(function(e){
                    window.location.href = "apply";
                    e.preventDefault();
                })
            }
        }
    });
})(django.jQuery);