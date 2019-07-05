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
		if(!this.node_dict[value]){
			throw "Cannot delete something from a HashCircularDoublyLinkedList that doesn't exist";
		}
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
	update_value(old_val, new_val){
		var node = this.node_dict[old_val];
		if(!node){
			alert(old_val, new_val, node);
		}
		node.value = new_val;
	}
	listify(){
		var output = [this.head.value];
		var node = this.head.next;
		while(node != this.head){
			output.push(node.value);
			node = node.next;
		}
		return output;
	}
}