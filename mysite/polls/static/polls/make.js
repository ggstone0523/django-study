n = 1;
    
$("#add_button").click(function() {
    n = n + 1;
    if (n <= 3) {
        $("input[name=choices_number]").attr('value', n)

        $("#remove_button").last().remove();

        newInputText =
        '<div id="row_input"> <label for="choice' + n + '" class="form-label">Enter your choice ' + n + ': </label>' +
        '<div class="input-group mb-3">' +
        '<input type="text" name="choice_text' + n + '" id="choice' + n + '" class="form-control" required>' + 
        '<button type="button" id="remove_button" class="btn btn-outline-secondary">Remove</button> </div> </div>';

        $('#newInput').append(newInputText);
    } else {
        alert('Choice limits is three.');
        n = n - 1;
    }
});

$("body").on("click", "#remove_button", function () {
    $(this).parents("#row_input").remove();

    n = n - 1;
    $("input[name=choices_number]").attr('value', n);

    if (n != 1)
        $(".input-group").last().append('<button type="button" id="remove_button" class="btn btn-outline-secondary">Remove</button>')
})