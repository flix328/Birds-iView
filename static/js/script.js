/*

var testDLL = new HashCircularDoublyLinkedList(["asd"]);
testDLL.insert_end(1);
testDLL.insert_end(2);
testDLL.insert_end(3);

test_list = testDLL.listify();

alert(test_list);

testDLL.delete_value(2);
test_list = testDLL.listify();
alert(test_list);

*/

var map = L.map('mapid').setView([0, 0], 2);

var polycoords = new HashCircularDoublyLinkedList([]);
var polygon = L.polygon([]).addTo(map);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
	maxZoom: 20, /* changed from original 18*/
	attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
		'<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
		'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
	id: 'mapbox.satellite'
}).addTo(map);

function onMarkerClick(e) {
    map.removeLayer(this);
}


function onMarkerDrag(e){
	// use e.oldLatLng;
	polycoords.update_value(e.oldLatLng, e.latlng);
	map.removeLayer(polygon);
	polygon = L.polygon(polycoords.listify()).addTo(map);
}

function onMapClick(e) {
	var marker = L.marker(e.latlng, {draggable: 'true', title: e.latlng, autoPan: 'true', autoPanPadding: [60, 50]}).addTo(map).on('click', onMarkerClick);
	// add to existing polygon
	polycoords.insert_end(e.latlng);
	//alert(e.latlng);
	//polycoords.push(e.latlng);
	map.removeLayer(polygon);
	marker.on('drag', onMarkerDrag);
	polygon = L.polygon(polycoords.listify()).addTo(map);
}



//map.on('click', onMapClick);

var dbl_click_timeout = 200; // in milliseconds
var click_start = 0;
var num_clicks = 0;
map.on('click', function(event){
	var d = new Date();
	var cur_time = d.getTime();
	
	if(cur_time - click_start > dbl_click_timeout){
		num_clicks = 1;
		click_start = cur_time;
		setTimeout(function () {
					if(num_clicks == 1){
						onMapClick(event);
					}}, dbl_click_timeout);
	}
	else {
		click_start = cur_time;
		num_clicks++;
		map.zoomIn();
	}
	
	click_start = cur_time;
});






var controlID = document.getElementById("controls");
L.DomEvent.disableClickPropagation(controlID); 
L.DomEvent.disableScrollPropagation(controlID); 


$( function() {
	$( "#slider-vertical" ).slider({
		orientation: "vertical",
		range: "min",
		min: 20,
		max: 120,
		value: 60,
		slide: function( event, ui ) {
			$( "#amount" ).val( ui.value );
		}
    });
	$( "#amount" ).val( $( "#slider-vertical" ).slider( "value" ) );
} );

