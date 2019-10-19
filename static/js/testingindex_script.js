$(document).keyup(function(e) {
     if (e.key === "Escape") { // escape key maps to keycode `27`
        hide_sidebar();
    }
});

sidebar = document.getElementById('sidebar');
function show_sidebar(){
    sidebar.classList.remove('exit');
    sidebar.classList.add('enter');
}

function hide_sidebar(){
    sidebar.classList.remove('enter');
    sidebar.classList.add('exit');
}