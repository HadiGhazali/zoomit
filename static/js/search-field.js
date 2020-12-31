
$('#search-icon-2').css('cursor', 'pointer');

$("#search-icon-2").click(function () {
    $('#search-field-2').css('display', 'block')
    $(this).css('display', 'none')
    $('#close-search-field-2').css({'display': 'block','cursor':'pointer'})
})

$('#close-search-field-2').click(function () {
    $('#search-field-2').css('display', 'none')
    $(this).css({'display': 'none'})
    $('#search-icon-2').css('display', 'block')
})
