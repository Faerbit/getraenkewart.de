$(document).ready(function() {
    $('input').on('input', function() {
        var summe = parseInt($(this).parent().parent().find('#summand').text()) + parseInt($(this).val())
        if (isNaN(summe))
            summe = $(this).parent().parent().find('#summand').text()
        $(this).parent().parent().find("#summe").text(summe);
    });
    $('#add-button').on("click", function() {
        var content = '<tr><td><div class="row"> <div class="col-md-2"><button class="btn btn-success">&#10004;</button></div><p class="form-control-static col-md-10">asdf</p></div><td></td><td></td><td></td></tr>';
        $('.table tr:last').after(content);
        $(this).remove()
    });
});
