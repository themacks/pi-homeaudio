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
//Inactive - 5sec up to 10sec
var timeout = 5000;
var statusActive = true;
function statusCheck(){
    $.ajax({
            url: './status',
            dataType: 'json',
            cache: false,
            success: statusHandle,
            complete: function() {
                if (statusActive){
                    setTimeout(statusCheck, timeout);
                }
                }
            });            
}

//Function to handle status update. 
function statusHandle(data){

    //as long as we are processing the status we don't want another to fire
    statusActive = false;
    
    $.mobile.changePage( "./pandora#login", { transition: "pop"} );
    //alert('Received: '+data);
}

