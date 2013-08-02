//
//  jQuery Pandora application
//
//  mark mccarthy
//
//


$(document).ready( function() {
    //Start periodic ajax request to check for status updates
    statusCheck();

});

//Function to check for status updates
//Interval between check varies on apps current state
//Initial - 1sec
//Playing - 0.5sec
//Inactive - 5sec
function statusCheck(){
    $.ajax({
            url: './status',
            dataType: 'json',
            cache: false,
            success: statusHandle,
            complete: function() {
                setTimeout(statusCheck, 5000);
                }
            });            
}

//Function to handle status update. 
function statusHandle(data){
    alert('Received: '+data);
}

