function getDocHeight() {
    var D = document;
    return Math.max(
        D.body.scrollHeight, D.documentElement.scrollHeight,
        D.body.offsetHeight, D.documentElement.offsetHeight,
        D.body.clientHeight, D.documentElement.clientHeight
    )
}

var travel_span = 0.3;
function amountscrolled(){
    var winheight = window.innerHeight || (document.documentElement || document.body).clientHeight;
    var docheight = getDocHeight();
    var scrollTop = window.pageYOffset || (document.documentElement || document.body.parentNode || document.body).scrollTop;
    var trackLength = docheight - winheight;
    var pctScrolled = Math.min(scrollTop/480,1); // gets percentage scrolled (ie: 80 or NaN if tracklength == 0)
	document.getElementById("drone_photo_img").style.marginLeft = (-144 - 0.5 * travel_span * window.innerWidth + pctScrolled * travel_span * window.innerWidth).toString() + "px";
}
amountscrolled();
 
window.addEventListener("scroll", function(){
    amountscrolled();
}, false)