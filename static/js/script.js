class Node {
	constructor(value){
		this.value = value;
		this.prev = this;
		this.next = this;
	}
}

class HashCircularDoublyLinkedList {
	// This is a special Circular Doubly Linked List that allows you to delete nodes by their value
	// therefore no two values can be the same
	constructor(values=null){
		this.node_dict = {}	// maps a value to its Node object
		if(values.length == 0){
			this.head = null;
		}
		else{
			for(var i=0; i<values.length; i++){
				var value = values[i];
				this.insert_end(value);
			}
		}
		
	}
	insert_end(value){
		if(this.node_dict[value]){
			throw "Cannot store two identical values in a HashCircularDoublyLinkedList";
		}
		var new_node = new Node(value);
		if(this.head == null){
			new_node.prev = new_node;
			new_node.next = new_node;
			this.head = new_node;
		}
		else {
			var last = this.head.prev;
			new_node.next = this.head;
			this.head.prev = new_node;
			new_node.prev = last;
			last.next = new_node;
		}
		this.node_dict[value] = new_node;
	}
	delete_value(value){
		var node = this.node_dict[value];
		this.delete_node(node);
	}
	delete_node(node){
		var prev_node = node.prev;
		var next_node = node.next;
		prev_node.next = next_node;
		next_node.prev = prev_node;
		if(node == this.head){
			this.head = next_node;
		}
	}
}

var testDLL = new HashCircularDoublyLinkedList([]);
testDLL.insert_end(1);
testDLL.insert_end(2);
testDLL.insert_end(3);
alert(testDLL.head.value);
alert(testDLL.head.next.value);
alert(testDLL.head.next.next.value);

testDLL.delete_value(1);
alert(testDLL.head.value);
alert(testDLL.head.next.value);



var map = L.map('mapid').setView([0, 0], 2);

var polycoords = []
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
	//keofjweiofj.
}

function onMapClick(e) {
	var marker = L.marker(e.latlng, {draggable: 'true', title: e.latlng, autoPan: 'true', autoPanPadding: [60, 50]}).addTo(map).on('click', onMarkerClick);
	// add to existing polygon
	polycoords.push(e.latlng)
	map.removeLayer(polygon);
	marker.on('drag', onMarkerDrag);
	polygon = L.polygon(polycoords).addTo(map);
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

