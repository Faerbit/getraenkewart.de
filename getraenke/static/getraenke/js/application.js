$(document).ready(function() {
    $("input").each(updateSum);
    $('input').on('input', updateSum);
    $('#add-button').on("click", function() {
        $(".table tr:last").show();
        $(this).hide();
    });
});

function updateSum (){
    var summe = +$(this).closest("td").find('#summand').text() + +$(this).val();
    if (isNaN(summe))
        summe = $(this).closest("td").find('#summand').text();
    $(this).closest("td").find("#summe").text(summe);
}
