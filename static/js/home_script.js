function getDocHeight() {
    var D = document;
    return Math.max(
        D.body.scrollHeight, D.documentElement.scrollHeight,
        D.body.offsetHeight, D.documentElement.offsetHeight,
        D.body.clientHeight, D.documentElement.clientHeight
    )
}

var travel_span = 0.3;
function onScroll(){
    var winheight = window.innerHeight || (document.documentElement || document.body).clientHeight;
    var docheight = getDocHeight();
    var scrollTop = window.pageYOffset || (document.documentElement || document.body.parentNode || document.body).scrollTop;
    var trackLength = docheight - winheight;
    var pctScrolled = Math.min(scrollTop/480,1);
	document.getElementById("drone_photo_img").style.marginLeft = (travel_span * window.innerWidth * (pctScrolled - 0.5) - 144).toString() + "px";
}
onScroll();
document.getElementById("drone_photo_img").style.display = "block";

window.addEventListener("scroll", onScroll, false)
window.addEventListener("resize", onScroll, false)