$(function() {
    $("input[name=photo_file]").change(function() {
        $(this).parents("label").addClass("disabled");
        $(this).parents("form").submit();
        $(this).prop("disabled", "true");
    });

    $(".button-collapse").sideNav();

    $(".requirement-row").click(function() {
        $("#editmodal").find("label[for=edit_requirement_description]").addClass("active");
        $("#editmodal").find("#edit_requirement_description").attr("value", $(this).children(".requirement-description").text());
        $("#editmodal").find("label[for=edit_requirement_difficulty]").addClass("active");
        $("#editmodal").find("#edit_requirement_difficulty").attr("value", $(this).children(".requirement-difficulty").text());
        if ($(this).children(".requirement-is-basic").children("i").length) {
            $("#editmodal").find("#edit_requirement_is_basic").attr("checked", "checked");
        } else {
            $("#editmodal").find("#edit_requirement_is_basic").removeAttr("checked");
        }
        $("#editmodal").find("#edit_requirement_id").attr("value", $(this).attr("data-id"));
        $("#editmodal").openModal();
    });
});
