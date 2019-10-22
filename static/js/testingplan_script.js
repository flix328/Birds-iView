MAX_PHOTOS = 99;

var map = L.map('mapid').setView([-41,173], 6);
map.doubleClickZoom.disable();
map.on('click', onMapClick);

var poly_data = [];

var map_layer = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
	maxZoom: 20,
	attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
		'<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
		'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
	id: 'mapbox.satellite'
}).addTo(map);

is_satellite = true;
function onMapTypeClick(){
	if(is_satellite){
		map.removeLayer(map_layer);
		map_layer = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
			maxZoom: 20,
			attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
				'<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
				'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
			id: 'mapbox.streets'
		}).addTo(map);


		$("#map_type a").text('Satellite');
		document.getElementById("map_type_a").style.backgroundImage = "url('/static/images/mapbox_satellite.png')";
	}
	else{
		map.removeLayer(map_layer);
		map_layer = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
			maxZoom: 20,
			attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
				'<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
				'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
			id: 'mapbox.satellite'
		}).addTo(map);
		$("#map_type a").text('Streets');
		document.getElementById("map_type_a").style.backgroundImage = "url('/static/images/mapbox_streets.png')";
	}
	is_satellite = !is_satellite;
}

var polyIcon = L.icon({

	iconUrl: "/static/images/poly_marker.png",

	iconSize:     [15, 15], // size of the icon
	iconAnchor:   [7.5, 7.5], // point of the icon which will correspond to marker's location
	popupAnchor:  [0, 0] // point from which the popup should open relative to the iconAnchor
});

var pathIcon = L.icon({

	iconUrl: "/static/images/path_marker.png",

	iconSize:     [8, 8], // size of the icon
	iconAnchor:   [4, 4], // point of the icon which will correspond to marker's location
	popupAnchor:  [0, 0] // point from which the popup should open relative to the iconAnchor
});

var extra_pathIcon = L.icon({

	iconUrl: "/static/images/extra_path_marker.png",

	iconSize:     [8, 8], // size of the icon
	iconAnchor:   [4, 4], // point of the icon which will correspond to marker's location
	popupAnchor:  [0, 0] // point from which the popup should open relative to the iconAnchor
});


var poly_marker_keys = {icon: polyIcon, draggable: true, autoPan: true, autoPanPadding: [60, 50]};
var poly_markers = L.layerGroup().addTo(map);
var poly_shape = L.polygon([], {fillColor: '#3d8ea1', fillOpacity: 0.2, color: '#3d8ea1'}).addTo(map);

function onMarkerClick(e) {
	if(is_busy){ return; }
	is_busy = true;

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
	map.removeLayer(e.target);
	poly_data = result;
	poly_shape.setLatLngs(poly);

	update_path();

	is_busy = false;
}

function onMarkerDragend(e){
	if(is_busy){ return; }
	is_busy = true;

	_id = e.target._leaflet_id

	poly = [];
	for (var i = 0; i < poly_data.length; i=i+1) {
		if(poly_data[i][0] == _id){
			poly_data[i][1] = e.target._latlng.lat
			poly_data[i][2] = e.target._latlng.lng
		}
		poly.push([poly_data[i][1], poly_data[i][2]]);
	}
	poly_shape.setLatLngs(poly);

	update_path();

	is_busy = false;
}

var is_busy = false;
function onMapClick(e) {
	console.log("starting onMapClick function");
	// if website is not busy
	if(is_busy){ return; }
	is_busy = true;

	var marker = L.marker(e.latlng, poly_marker_keys).addTo(poly_markers);
	marker.on('click', onMarkerClick);
	$.getJSON('/onMapClick',{poly_data: poly_data.toString(), lat: e.latlng.lat, lng: e.latlng.lng, _id: marker._leaflet_id}, function(data) {
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
		marker.on('dragend', onMarkerDragend);
		poly_shape.setLatLngs(poly);
		update_path();
		console.log("finishing the onMapClick section thing");
	});
	console.log("finishing onMapClick function");
}

var path_data = [];
var path_shape = L.polyline([], {color: '#FF3B3F', dashArray: "12 6"}).addTo(map);
var path_markers = L.layerGroup().addTo(map);
var extra_path_shape = L.polyline([], {color: '#515151', dashArray: "9 9"}).addTo(map);

function update_path(){
	is_busy = true;
	if(poly_data.length < 3){
		path_markers.clearLayers();
		path_data = [];
		path_shape.setLatLngs([]);
		extra_path_shape.setLatLngs([]);


		$("#stat_area").text('Survey Area: None');
		$("#stat_dist").text('Flight Distance: None');
		$("#stat_num_photos").text('Number of Photos: None');
		is_busy = false;
		return;
	}
	var altitude = parseFloat(document.getElementById("altitude_value").value.slice(0, -1));
	var heading = parseFloat(document.getElementById("heading_value").value.slice(0, -1));
	var overlap = parseFloat(document.getElementById("overlap_value").value.slice(0, -1)) * 0.01;
	var resolution = document.getElementById("resolution_input").value;
	var view_angle = parseFloat(document.getElementById("view_angle_input").value);



	$.getJSON('/updatePath',{altitude: altitude, heading: heading, overlap: overlap, resolution: resolution, view_angle: view_angle, poly_data: poly_data.toString()}, function(data) {
		is_busy = true;
		data = data.toString().split(",");
		var poly_area_str = (parseFloat(data[0]).toPrecision(2) / 1000000).toString() + "km²";
		var dist_str = (parseFloat(data[1]).toPrecision(2) / 1000).toString() + "km";
		var num_photos_str = data[2].toString();
		if(parseFloat(data[2]) > MAX_PHOTOS){
			num_photos_str = MAX_PHOTOS.toString() + "+"
		}


		$("#stat_area").text('Survey Area: ' + poly_area_str);
		$("#stat_dist").text('Flight Distance: ' + dist_str);
		$("#stat_num_photos").text('Number of Photos: ' + num_photos_str);

		var path = [];
		for(var i = 3; i < data.length; i=i+2){
			lat = parseFloat(data[i]);
			lng = parseFloat(data[i+1]);
			path.push([lat, lng]);
		}
		path_shape.setLatLngs(path.slice(0, MAX_PHOTOS));
		extra_path_shape.setLatLngs(path.slice(MAX_PHOTOS-1,path.length));
		map.removeLayer(path_markers);
		path_markers = L.layerGroup().addTo(map);
		for(var i=0; i<Math.min(path.length,MAX_PHOTOS); i++){
			L.marker(path[i], {icon:pathIcon, draggable: false}).addTo(path_markers);
		}
		for(var i=MAX_PHOTOS; i<path.length; i++){
			L.marker(path[i], {icon:extra_pathIcon, draggable: false}).addTo(path_markers);
		}
		path_data = path;
		is_busy = false;
	});
}


var controlID = document.getElementById("controls");
L.DomEvent.disableClickPropagation(controlID);
L.DomEvent.disableScrollPropagation(controlID);
var map_typeID = document.getElementById("map_type");
L.DomEvent.disableClickPropagation(map_typeID);
L.DomEvent.disableScrollPropagation(map_typeID);
var summary_boxID = document.getElementById("summary_box");
L.DomEvent.disableClickPropagation(summary_boxID);
L.DomEvent.disableScrollPropagation(summary_boxID);

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
		},
		stop: function( event, ui ) {
			on_update();
		},
    });
} );

$( function() {
	$( "#heading_slider" ).slider({
		orientation: "vertical",
		range: false,
		min: 0,
		max: 180,
		value: 0,
		create: function( event, ui ) {
			document.getElementById("heading_value").value = "0°";
		},
		slide: function( event, ui ) {
			document.getElementById("heading_value").value = ui.value.toString() + "°";
		},
		stop: function( event, ui ) {
			on_update();
		},
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
		},
		stop: function( event, ui ) {
			on_update();
		},

    });
} );

function onClearClick() {
	console.log("starting onClearClick function");
	if(is_busy){ return; }
	is_busy = true;

	poly_data = [];
	poly_shape.setLatLngs([]);
	poly_markers.clearLayers();
	update_path();
	console.log("finishing onClearClick function");
}
var adjusting_altitude = false;
function onAltitudeClick(){
	if(!adjusting_altitude){
		reset_adjust_boxes();
		disable_adjust_labels();
		document.getElementById('altitude_btn').style.borderTopRightRadius = "0";
		document.getElementById('birds_btn').style.borderBottomRightRadius = "0";
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
var adjusting_heading = false;
function onHeadingClick(){
	if(!adjusting_heading){
		reset_adjust_boxes();
		disable_adjust_labels();
		document.getElementById('altitude_btn').style.borderTopRightRadius = "0";
		document.getElementById('birds_btn').style.borderBottomRightRadius = "0";
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
var adjusting_overlap = false;
function onOverlapClick(){
	if(!adjusting_overlap){
		reset_adjust_boxes();
		disable_adjust_labels();
		document.getElementById('altitude_btn').style.borderTopRightRadius = "0";
		document.getElementById('birds_btn').style.borderBottomRightRadius = "0";
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
var adjusting_camera = false;
function onCameraClick(){
	if(!adjusting_camera){
		reset_adjust_boxes();
		disable_adjust_labels();
		document.getElementById('camera_box').style.display = "block";
		document.getElementById('birds_btn').style.borderBottomRightRadius = "0";

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
var adjusting_birds = false;
function onBirdClick(){
	if(!adjusting_birds){
		reset_adjust_boxes();
		disable_adjust_labels();
		document.getElementById('altitude_btn').style.borderTopRightRadius = "0";
		document.getElementById('birds_btn').style.borderBottomRightRadius = "0";
		document.getElementById('bird_box').style.display = "block";
		document.getElementById("bird_input").focus();

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
	document.getElementById('altitude_btn').style.borderTopRightRadius = "5px";
	document.getElementById('birds_btn').style.borderBottomRightRadius = "5px";
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


// Initializing the Bird class
class Bird {
    constructor(name, size) {
        this.name = name;
        this.size = size;
    }
}

var birds = {};
function get_birds(){
    var is_done = false;
    $.getJSON('/getBirds',{}, function(data) {
        data = data.split(",");
        for(var i=0;i<data.length;i=i+2){
            name = data[i];
            size = parseInt(data[i+1]);
            bird = new Bird(name, size);
            birds[name] = bird;
        }
    });
}
get_birds();

function simplify_string(str){
	words = str.toLowerCase().trim().split(/\s+/);
	str = words.join(" ");
	return str;
}

function check_bird_complete(){
	bird_input = document.getElementById("bird_input").value;
	bird_input = simplify_string(bird_input);

	var result = ""

	var matches = [];
	for(var bird_name in birds){
		if(simplify_string(bird_name) == bird_input){
			matches.push(bird_name);
		}
	}
	if(matches.length == 1){
		result = matches[0];
	}
	else{
		matches = [];
	    for(var bird_name in birds){
			if(simplify_string(bird_name).startsWith(bird_input)){
				matches.push(bird_name);
			}
		}
		if(matches.length == 1){
			result = matches[0];
		}
		else{
			matches = [];
	        for(var bird_name in birds){
				if(simplify_string(bird_name).includes(bird_input)){
					matches.push(bird_name);
				}
			}
			if(matches.length == 1){
				result = matches[0];
			}
		}
	}
	complete_input = document.getElementById("bird_complete");
	if(result != ""){
		complete_input.value = result;
		complete_input.style.visibility = "visible";
	}
	else{
		complete_input.value = "";
		complete_input.style.visibility = "hidden";

	}
}

$("#bird_input").on('keydown input paste change', function(){ /*keydown input paste change */
      check_bird_complete();
});

$("#bird_input").on('keyup', function (e) {
    if (e.keyCode === 13) {
        add_bird();
    }
});

var birds_used = [];
function add_bird(){
	bird_name = document.getElementById("bird_complete").value;
	if(bird_name != ""){
		if(!birds_used.includes(bird_name)){
			birds_used.push(bird_name);
			$("#bird_list").append('<li ondblclick="remove_bird(' + "'" + bird_name.toString() + "'" + ')">' + bird_name.toString() + '</li>');
		}
		document.getElementById("bird_input").value = "";
		check_bird_complete();
	}

	document.getElementById("bird_input").focus();
	check_birds();
}

function remove_bird(bird_name){
	var index = birds_used.indexOf(bird_name);

	var bird_list = document.getElementById("bird_list")
	bird_list.removeChild(bird_list.childNodes[index]);
	birds_used.splice(index, 1);
}

function extract_resolution(str){
	parts = str.split("x");
	if(parts.length == 2 && !isNaN(parts[0]) && !isNaN(parts[1])){
		var res_w = parseFloat(parts[0]);
		var res_h = parseFloat(parts[1]);
		if(res_w > 0 && res_h > 0){
			return [res_w, res_h];
		}
	}
}

var resolution = [960, 640];
function on_resolution_value_change(){
	res = extract_resolution(document.getElementById("resolution_input").value);
	if(res){
		resolution = res;
	}
	else{
		document.getElementById("resolution_input").value = resolution[0].toString() + "x" + resolution[1].toString();
	}
	on_update();
}

var view_angle = 104.4;
function on_view_angle_value_change(){
	str = document.getElementById("view_angle_input").value;
	if(isNaN(str) || parseFloat(str) <= 0 || parseFloat(str) >= 180){
		document.getElementById("view_angle_input").value = view_angle.toString();
	}
	else{
		view_angle = parseFloat(str);
	}
	on_update();
}

$("#resolution_input").focusout(function(){
	on_resolution_value_change();
	on_update();
});
$("#view_angle_input").focusout(function(){
	on_view_angle_value_change();
	on_update();
});

document.getElementById("resolution_input").onblur=on_resolution_value_change;
$("#resolution_input").on('keyup', function (e) {
    if (e.keyCode === 13) {
        on_resolution_value_change();
        on_update();
    }
});
document.getElementById("view_angle_input").onblur=on_resolution_value_change;
$("#view_angle_input").on('keyup', function (e) {
    if (e.keyCode === 13) {
		on_view_angle_value_change();
        on_update();
    }
});

function check_birds(){
	h = parseFloat(document.getElementById("altitude_value").value.slice(0, -1));
	a = parseFloat(document.getElementById("view_angle_input").value);
	var res = extract_resolution(document.getElementById("resolution_input").value);
	var res_w = res[0];
	var res_h = res[1];
	G = 2 * h * Math.tan(a / 2  * Math.PI/180) / Math.sqrt(Math.pow(res_w, 2) + Math.pow(res_h, 2)) * 100

	for(var i=0; i<birds_used.length; i++){
		size = birds[birds_used[i]].size;
		if(G < 0.5 * size){
			bird_list.childNodes[i].style.backgroundColor = "rgba(0, 255, 0, 0.15)";
		}
		else if(G < size){
			bird_list.childNodes[i].style.backgroundColor = "rgba(255, 165, 0, 0.15)";
		}
		else{
			bird_list.childNodes[i].style.backgroundColor = "rgba(255, 0, 0, 0.15)";
		}
	}
}

function on_update(){
	check_birds();
	update_path();
}

function download_csv() {
    var csv = 'Name,Title\n';
    data.forEach(function(row) {
            csv += row.join(',');
            csv += "\n";
    });

    var hiddenElement = document.createElement('a');
    hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv);
    hiddenElement.target = '_blank';
    hiddenElement.download = 'people.csv';
    hiddenElement.click();
}

function onExportClick(){
	var altitude = parseFloat(document.getElementById("altitude_value").value.slice(0, -1));
	var heading = parseFloat(document.getElementById("heading_value").value.slice(0, -1));

	var csv = "latitude,longitude,altitude(m),heading(deg),curvesize(m),rotationdir,gimbalmode,gimbalpitchangle,actiontype1,actionparam1,actiontype2,actionparam2,actiontype3,actionparam3,actiontype4,actionparam4,actiontype5,actionparam5,actiontype6,actionparam6,actiontype7,actionparam7,actiontype8,actionparam8,actiontype9,actionparam9,actiontype10,actionparam10,actiontype11,actionparam11,actiontype12,actionparam12,actiontype13,actionparam13,actiontype14,actionparam14,actiontype15,actionparam15,altitudemode,speed(m/s),poi_latitude,poi_longitude,poi_altitude(m),poi_altitudemode,photo_timeinterval\n";


	for(var i=0; i<Math.min(path_data.length, MAX_PHOTOS); i++){
		var lat = path_data[i][0];
		var lon = path_data[i][1];

		row = lat.toString() + "," + lon.toString() + "," + altitude.toString() + "," + heading.toString() + ",0,0,0,0,";
		if(i==0){
			row += "5,-90,"
		}
		row += "1,0,"
		csv += row + "\n";
	}

	var hiddenElement = document.createElement('a');
    hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv);
    hiddenElement.target = '_blank';
    hiddenElement.download = 'birds_iview_flight_path.csv';
    hiddenElement.click();
}


function savePlan(){
    var point_list = "";
    for(var i=0; i < poly_data.length; i++){
        point_list = point_list + poly_data[i][1] + "," + poly_data[i][2] + ",";
    }
    point_list = point_list.slice(0, -1);


    result_data = {
        name: Math.random().toString(),
        altitude: parseFloat(document.getElementById("altitude_value").value.slice(0, -1)),
        heading: parseFloat(document.getElementById("heading_value").value.slice(0, -1)),
        overlap: parseFloat(document.getElementById("overlap_value").value.slice(0, -1)) * 0.01,
        resolution: document.getElementById("resolution_input").value,
        view_angle: parseFloat(document.getElementById("view_angle_input").value),
        bird_list: birds_used.toString(),
        location: map.getCenter().lat.toString() + ", " + map.getCenter().lng.toString(),
        zoom_level: map.getZoom(),
        point_list: point_list
    }
    $.getJSON('/savePlan',result_data, function(data) {

		console.log("did the save thing");
	});
}