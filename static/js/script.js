var map = L.map('mapid').setView([-43.4651629,172.6058556], 17);
map.doubleClickZoom.disable(); 
map.on('click', onMapClick);

var poly_data = [];

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
	maxZoom: 20, /* changed from original 18*/
	attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
		'<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
		'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
	id: 'mapbox.satellite'
}).addTo(map);

var poly_shape = L.polygon([]).addTo(map);

function onMarkerClick(e) {
	var _id = e.target._leaflet_id;
	var i = 0;
	result = [];
	poly = [];
	for (var i = 0; i < poly_data.length; i=i+1) {
		if(poly_data[i][0] != _id){
			result.push(poly_data[i]);
			poly.push([poly_data[i][1],poly_data[i][2]]);
		}
	}
	poly_data = result;
	map.removeLayer(poly_shape);
	map.removeLayer(e.target);
	poly_shape = L.polygon(poly).addTo(map);
	
	update_path();
}

function onMarkerDragend(e){
	_id = e.target._leaflet_id
	
	poly = [];
	for (var i = 0; i < poly_data.length; i=i+1) {
		if(poly_data[i][0] == _id){
			poly_data[i][1] = e.target._latlng.lat
			poly_data[i][2] = e.target._latlng.lng
		}
		poly.push([poly_data[i][1], poly_data[i][2]]);
	}
	map.removeLayer(poly_shape);
	poly_shape = L.polygon(poly).addTo(map);
	
	update_path();
}

function onMapClick(e) {
	var marker = L.marker(e.latlng, {draggable: 'true', title: e.latlng, autoPan: 'true', autoPanPadding: [60, 50]})
	marker.addTo(map)
	marker.on('click', onMarkerClick);
	
	$.getJSON('/onMapClick',{poly: poly_data.toString(), lat: e.latlng.lat, lng: e.latlng.lng, _id: marker._leaflet_id}, function(data) {
		data = data.toString().split(",");
		for(var i = 0; i < data.length; i=i+1){
			data[i] = parseFloat(data[i]);
		}
		poly = [];
		poly_data = [];
		for (var i = 0; i < data.length; i=i+3) {
			poly.push([data[i+1], data[i+2]]);
			poly_data.push([data[i], data[i+1], data[i+2]]);
		}
		map.removeLayer(poly_shape);
		marker.on('dragend', onMarkerDragend);
		poly_shape = L.polygon(poly).addTo(map);
		update_path();
	});
	
}

var path_data = [];
var path_shape = L.polyline([], {color: 'red'}).addTo(map);

function update_path(){
	$.getJSON('/updatePath',{poly: poly_data.toString()}, function(data) {
		data = data.toString().split(",");
		bearing = parseFloat(data[0]);
		path = [];
		for(var i = 1; i < data.length; i=i+2){
			lat = parseFloat(data[i]);
			lng = parseFloat(data[i+1]);
			path.push([lat, lng]);
		}
		map.removeLayer(path_shape);
		path_shape = L.polyline(path, {color: 'red'}).addTo(map);
	});
	
}

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

