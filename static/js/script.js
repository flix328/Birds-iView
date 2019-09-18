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


var blueIcon = L.icon({
	
	iconUrl: "/static/images/marker_icon.png",
	//shadowUrl: 'leaf-shadow.png',

	iconSize:     [15, 15], // size of the icon
	//shadowSize:   [50, 64], // size of the shadow
	iconAnchor:   [7.5, 7.5], // point of the icon which will correspond to marker's location
	//shadowAnchor: [4, 62],  // the same for the shadow
	popupAnchor:  [0, 0] // point from which the popup should open relative to the iconAnchor
});

var marker_keys = {icon: blueIcon, draggable: 'true', autoPan: 'true', autoPanPadding: [60, 50]};
var poly_keys = {fillColor: '#3d8ea1', fillOpacity: 0.2, color: '#3d8ea1'};
var poly_shape = L.polygon([], poly_keys).addTo(map);

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
	poly_shape = L.polygon(poly, poly_keys).addTo(map);
	
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
	poly_shape = L.polygon(poly, poly_keys).addTo(map);
	
	update_path();
}

function onMapClick(e) {
	var marker = L.marker(e.latlng, Object.assign({}, marker_keys, {title: e.latlng}));
	marker.addTo(map);
	marker.on('click', onMarkerClick);
	var out_str = "0, " + poly_data.toString();
	
	$.getJSON('/onMapClick',{poly: out_str, lat: e.latlng.lat, lng: e.latlng.lng, _id: marker._leaflet_id}, function(data) {
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
		poly_shape = L.polygon(poly, poly_keys).addTo(map);
		update_path();
	});
	
}

var path_data = [];
var path_keys = {color: '#FF3B3F', dashArray: "12 6"};
var path_shape = L.polyline([], path_keys).addTo(map);

$( function() {
	$( "#slider-vertical" ).slider({
		orientation: "vertical",
		range: "min",
		min: 20,
		max: 120,
		value: 60,
		slide: function( event, ui ) {
			document.getElementById("amount").value = ui.value.toString() + "m";
		},
		stop: function( event, ui ) {
			update_path();
		},
		create: function( event, ui ) {
			document.getElementById("amount").value = "60m";
		}
    });
} );

function update_path(){
	var altitude = 60;//$("#slider-vertical").slider("value");
	var out_str = altitude.toString() + ", " + poly_data.toString();
	
	$.getJSON('/updatePath',{data: out_str}, function(data) {
		data = data.toString().split(",");
		bearing = parseFloat(data[0]);
		path = [];
		for(var i = 1; i < data.length; i=i+2){
			lat = parseFloat(data[i]);
			lng = parseFloat(data[i+1]);
			path.push([lat, lng]);
		}
		map.removeLayer(path_shape);
		path_shape = L.polyline(path, path_keys).addTo(map);
	});
	
}

var controlID = document.getElementById("controls");
L.DomEvent.disableClickPropagation(controlID); 
L.DomEvent.disableScrollPropagation(controlID); 



function clicky(){
	alert("yeet");
}