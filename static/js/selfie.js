$(function() {
    $("input[name=selfie_file]").change(function() {
        $(this).parents("form").submit();
	$(this).parents("label").addClass("disabled");
        $(this).prop("disabled", "true");
    });

    $('.collapsible').collapsible({ accordion: false });
    $('.collapsible .open-level').click();

    $(".button-collapse").sideNav();
});
