var mymap = L.map('mapid').setView([0, 0], 2);

var polycoords = []
var polygon = L.polygon([]).addTo(mymap);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
	maxZoom: 20, /* changed from original 18*/
	attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
		'<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
		'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
	id: 'mapbox.satellite'
}).addTo(mymap);

function onMarkerClick(e) {
    mymap.removeLayer(this);
}

function onMarkerDrag(e){
	//keofjweiofj
}

function onMapClick(e) {
	var marker = L.marker(e.latlng, {draggable: 'true', title: e.latlng, autoPan: 'true', autoPanPadding: [60, 50]}).addTo(mymap).on('click', onMarkerClick);
	// add to existing polygon
	polycoords.push(e.latlng)
	mymap.removeLayer(polygon);
	marker.on('drag', onMarkerDrag);
	polygon = L.polygon(polycoords).addTo(mymap);
}

mymap.on('click', onMapClick);


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

