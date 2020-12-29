// When the user scrolls down 20px from the top of the document, slide down the navbar

var prevScrollpos = window.pageYOffset;
window.onscroll = function () {
    let currentScrollPos = window.pageYOffset;

    if ($(document).width() > 976) {

        if (prevScrollpos > currentScrollPos) {
            document.getElementById("my-header").style.top = "0";
        } else {
            document.getElementById("my-header").style.top = "-56px";
        }
        prevScrollpos = currentScrollPos;
    }
    else {
         document.getElementById("my-header").style.top = "0";
    }
}