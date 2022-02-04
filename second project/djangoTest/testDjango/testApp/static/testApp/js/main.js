window.onscroll = function show_header ()
{
    var header = document.querySelector('.asd');
    if(window.pageYOffset > 10){
        header.classList.add('.header_fixed');
    }
    else
    {
        header.classList.remove('.header_fixed');
    }
}