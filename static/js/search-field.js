$('#search-icon').css('cursor', 'pointer');

$("#search-icon").click(function () {
    $('#search-field').css('display', 'block')
    $(this).css('display', 'none')
    $('#close-search-field').css({'display': 'block','cursor':'pointer'})
})

$('#close-search-field').click(function () {
    $('#search-field').css('display', 'none')
    $(this).css({'display': 'none'})
    $('#search-icon').css('display', 'block')
})

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