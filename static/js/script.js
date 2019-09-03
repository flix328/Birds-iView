var map = L.map('mapid').setView([-10.8669988,27.0927838], 11);
map.doubleClickZoom.disable(); 

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
	
	
	//i = 0;
	//while(poly_data[i][0] != _id){
		//if(i == poly_data.length -1){
		//	alert(_id)
		//	alert(poly_data)
		//}
		//i=i+1;
	//}
	//poly_data[i][1] = e.target._latlng.lat
	//poly_data[i][2] = e.target._latlng.lng
	
	//map.removeLayer(polygon);
	
	//polygon = L.polygon(polycoords.listify()).addTo(map);
	
}

function onMapClick(e) {
	var marker = L.marker(e.latlng, {draggable: 'true', title: e.latlng, autoPan: 'true', autoPanPadding: [60, 50]})
	marker.addTo(map)
	marker.on('click', onMarkerClick);
	
	// marker._leaflet_id, marker._latlng
	//alert(marker._latlng)
	//alert(marker._latlng.lat)
	//alert(marker._latlng.lng)
	
	
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
		//marker.on('drag', onMarkerDrag);
		marker.on('dragend', onMarkerDragend);
		poly_shape = L.polygon(poly).addTo(map);
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

