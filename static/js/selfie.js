$(function() {
    $("input[name=photo_file]").change(function() {
        $(this).parents("label").addClass("disabled");
        $(this).parents("form").submit();
        $(this).prop("disabled", "true");
    });

    $(".button-collapse").sideNav();
});
