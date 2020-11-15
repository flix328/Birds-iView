function export_flight_path(filename){
    console.log(filename);
}

function edit_flight_path(filename){
    console.log(filename);
}

function delete_flight_path(filename){
    $.getJSON('/deletePlan',{filename: filename}, function(data) {});
}