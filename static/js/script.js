var map = L.map('mapid').setView([-43.505835, 172.577879], 18);
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
var markerGroup = L.layerGroup().addTo(map);
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
	var marker = L.marker(e.latlng, Object.assign({}, marker_keys, {title: e.latlng})).addTo(markerGroup);
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





var adjusting_altitude = false;




$( function() {
	$( "#altitude_slider" ).slider({
		orientation: "vertical",
		range: false,
		min: 20,
		max: 120,
		value: 60,
		create: function( event, ui ) {
			document.getElementById("altitude_value").value = "60m";
		},
		slide: function( event, ui ) {
			document.getElementById("altitude_value").value = ui.value.toString() + "m";
		}/*,
		stop: function( event, ui ) {
			update_path();
		},
		*/
    });
} );

$( function() {
	$( "#heading_slider" ).slider({
		orientation: "vertical",
		range: false,
		min: 0,
		max: 360,
		value: 0,
		create: function( event, ui ) {
			document.getElementById("heading_value").value = "0°";
		},
		slide: function( event, ui ) {
			document.getElementById("heading_value").value = ui.value.toString() + "°";
		}/*,
		stop: function( event, ui ) {
			update_path();
		},
		*/
    });
} );

$( function() {
	$( "#overlap_slider" ).slider({
		orientation: "vertical",
		range: false,
		min: 0,
		max: 60,
		value: 0,
		create: function( event, ui ) {
			document.getElementById("overlap_value").value = "0%";
		},
		slide: function( event, ui ) {
			document.getElementById("overlap_value").value = ui.value.toString() + "%";
		}/*,
		stop: function( event, ui ) {
			update_path();
		},
		*/
    });
} );

function onClearClick() {
	map.removeLayer(markerGroup);
	markerGroup = L.layerGroup().addTo(map);
	poly_data = [];
	map.removeLayer(poly_shape);
	poly_shape = L.polygon([], poly_keys).addTo(map);
	path_data = [];
	map.removeLayer(path_shape);
	path_shape = L.polyline([], path_keys).addTo(map);
}
adjusting_altitude = false;
function onAltitudeClick(){
	if(!adjusting_altitude){
		reset_adjust_boxes();
		disable_adjust_labels();
		document.getElementById('altitude_btn').style.borderRadius = "5px 0 0 0";
		document.getElementById('birds_btn').style.borderRadius = "0 0 0 5px";
		document.getElementById('altitude_box').style.display = "block";
		
		document.getElementById('heading_btn').style.filter = "opacity(0.6) grayscale(1)";
		document.getElementById('overlap_btn').style.filter = "opacity(0.6) grayscale(1)";
		document.getElementById('camera_btn').style.filter = "opacity(0.6) grayscale(1)";
		document.getElementById('birds_btn').style.filter = "opacity(0.6) grayscale(1)";
		
		adjusting_altitude = true;
	}
	else{
		reset_adjust_boxes()
	}
}
adjusting_heading = false;
function onHeadingClick(){
	if(!adjusting_heading){
		reset_adjust_boxes();
		disable_adjust_labels();
		document.getElementById('altitude_btn').style.borderRadius = "5px 0 0 0";
		document.getElementById('birds_btn').style.borderRadius = "0 0 0 5px";
		document.getElementById('heading_box').style.display = "block";
		
		document.getElementById('altitude_btn').style.filter = "opacity(0.6) grayscale(1)";
		document.getElementById('overlap_btn').style.filter = "opacity(0.6) grayscale(1)";
		document.getElementById('camera_btn').style.filter = "opacity(0.6) grayscale(1)";
		document.getElementById('birds_btn').style.filter = "opacity(0.6) grayscale(1)";
		
		adjusting_heading = true;
	}
	else{
		reset_adjust_boxes();
		
	}
}
adjusting_overlap = false;
function onOverlapClick(){
	if(!adjusting_overlap){
		reset_adjust_boxes();
		disable_adjust_labels();
		document.getElementById('altitude_btn').style.borderRadius = "5px 0 0 0";
		document.getElementById('birds_btn').style.borderRadius = "0 0 0 5px";
		document.getElementById('overlap_box').style.display = "block";
		
		document.getElementById('altitude_btn').style.filter = "opacity(0.6) grayscale(1)";
		document.getElementById('heading_btn').style.filter = "opacity(0.6) grayscale(1)";
		document.getElementById('camera_btn').style.filter = "opacity(0.6) grayscale(1)";
		document.getElementById('birds_btn').style.filter = "opacity(0.6) grayscale(1)";
		
		adjusting_overlap = true;
	}
	else{
		reset_adjust_boxes();
	}
}
adjusting_camera = false;
function onCameraClick(){
	if(!adjusting_camera){
		reset_adjust_boxes();
		disable_adjust_labels();
		document.getElementById('camera_box').style.display = "block";
		
		document.getElementById('altitude_btn').style.filter = "opacity(0.6) grayscale(1)";
		document.getElementById('heading_btn').style.filter = "opacity(0.6) grayscale(1)";
		document.getElementById('overlap_btn').style.filter = "opacity(0.6) grayscale(1)";
		document.getElementById('birds_btn').style.filter = "opacity(0.6) grayscale(1)";
		
		adjusting_camera = true;
	}
	else{
		reset_adjust_boxes();
	}
}
adjusting_birds = false;
function onBirdClick(){
	if(!adjusting_birds){
		reset_adjust_boxes();
		disable_adjust_labels();
		document.getElementById('altitude_btn').style.borderRadius = "5px 0 0 0";
		document.getElementById('birds_btn').style.borderRadius = "0 0 0 5px";
		document.getElementById('bird_box').style.display = "block";
		
		document.getElementById('altitude_btn').style.filter = "opacity(0.6) grayscale(1)";
		document.getElementById('heading_btn').style.filter = "opacity(0.6) grayscale(1)";
		document.getElementById('overlap_btn').style.filter = "opacity(0.6) grayscale(1)";
		document.getElementById('camera_btn').style.filter = "opacity(0.6) grayscale(1)";
		
		adjusting_birds = true;
	}
	else{
		reset_adjust_boxes();
	}
}
function onExportClick(){
	alert("export");
}

function disable_adjust_labels(){
	var labels = document.getElementsByClassName("adjust_label");
	for(var i=0; i<labels.length; i++){
		labels[i].style.visibility = "hidden";
	}
}
function enable_adjust_labels(){
	var labels = document.getElementsByClassName("adjust_label");
	for(var i=0; i<labels.length; i++){
		labels[i].style.visibility = "visible";
	}
}

function reset_adjust_boxes(){
	adjusting_altitude = adjusting_heading = adjusting_overlap = adjusting_camera = adjusting_birds = false;
	document.getElementById('altitude_btn').style.borderRadius = "5px 5px 0 0";
	document.getElementById('birds_btn').style.borderRadius = "0 0 5px 5px";
	document.getElementById('altitude_box').style.display = "none";
	document.getElementById('heading_box').style.display = "none";
	document.getElementById('overlap_box').style.display = "none";
	document.getElementById('camera_box').style.display = "none";
	document.getElementById('bird_box').style.display = "none";
	document.getElementById('altitude_btn').style.filter = "opacity(1) grayscale(0)";
	document.getElementById('heading_btn').style.filter = "opacity(1) grayscale(0)";
	document.getElementById('overlap_btn').style.filter = "opacity(1) grayscale(0)";
	document.getElementById('camera_btn').style.filter = "opacity(1) grayscale(0)";
	document.getElementById('birds_btn').style.filter = "opacity(1) grayscale(0)";
	enable_adjust_labels();
}

$(document).keyup(function(e) {
     if (e.key === "Escape") { // escape key maps to keycode `27`
        reset_adjust_boxes()
    }
});