function manage_footer() {
    if ($(document).height() == $(window).height()) {
        $('footer').addClass('fixed-bottom');
        $('#footer-helper').height($('footer').height());
    } else {
        $('footer').removeClass('fixed-bottom');
        $('#footer-helper').height('0px');
    }
}
manage_footer()
window.addEventListener('resize', manage_footer, true);
$('.btn-close').click(() => {
    setTimeout(manage_footer, 200)
})

function get_min_sec(seconds) {
    minutes = parseInt(seconds / 60)
    seconds = seconds % 60
    return [minutes, seconds]
}

function startcountdown(seconds) {
    window.remaining = seconds;
    window.countdownInterval = setInterval(() => {
        seconds = window.remaining;
        minutes = parseInt(seconds / 60);
        seconds = seconds % 60;
        if (window.remaining < 1) {
            $('#submitform').show();
            $('#countdown').hide();
            clearInterval(window.countdownInterval)
        }
        else {
            $('#submitform').hide();
            $('#countdown').show();
        	$('#time').text(`${minutes.toLocaleString('en-US', {minimumIntegerDigits: 2})}:${seconds.toLocaleString('en-US', {minimumIntegerDigits: 2})}`);
        	window.remaining-=1
        }
    }, 1000)
}