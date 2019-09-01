var map = L.map('mapid').setView([0, 0], 2);
map.doubleClickZoom.disable(); 

var poly_coords = [];

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
	maxZoom: 20, /* changed from original 18*/
	attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
		'<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
		'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
	id: 'mapbox.satellite'
}).addTo(map);

var poly_shape = L.polygon([]).addTo(map);

function onMarkerClick(e) {
	var id = e.target._leaflet_id;
	var latlng = id_to_latlng[id];
	polycoords.delete_value(e.latlng);
	map.removeLayer(polygon);
	polygon = L.polygon(polycoords.listify()).addTo(map);
    map.removeLayer(this);
}


function onMarkerDrag(e){
	// use e.oldLatLng;
	map.removeLayer(polygon);
	
	polygon = L.polygon(polycoords.listify()).addTo(map);
	
}

function onMapClick(e) {
	var marker = L.marker(e.latlng, {draggable: 'true', title: e.latlng, autoPan: 'true', autoPanPadding: [60, 50]})
	marker.addTo(map)
	marker.on('click', onMarkerClick);
	
	// marker._leaflet_id, marker._latlng
	//alert(marker._latlng)
	//alert(marker._latlng.lat)
	//alert(marker._latlng.lng)
	
	
	$.getJSON('/onMapClick',{poly: poly_coords.toString(), lat: e.latlng.lat, lng: e.latlng.lng, _id: marker._leaflet_id}, function(data) {
		poly_coords = data
		map.removeLayer(poly_shape);
		//marker.on('drag', onMarkerDrag);
		//marker.on('dragend', onMarkerDrag);
		poly_shape = L.polygon(poly_coords).addTo(map);
	});
	
	
}
map.on('click', onMapClick);

// originalEvent,containerPoint,layerPoint,latlng,type,target,sourceTarget


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

