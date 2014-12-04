
function geolocate()
    {
         if (navigator.geolocation) 
            {
              navigator.geolocation.getCurrentPosition( TestMap, error, {maximumAge: 30000, timeout: 50000, enableHighAccuracy: true} );
        }
        else
        {
              alert("Sorry, but it looks like your browser does not support geolocation.");
        }
    }

function TestMap(position) {
	var latitude = position.coords.latitude;
	var longitude = position.coords.longitude;
	
	$( "input[name='lat']" ).val(latitude);
	$( "input[name='lon']" ).val(longitude);

	}
	
function error() {

		}
		
function detectTimezone() {
	var x = new Date();
	var currentTimeZoneOffsetInHours = x.getTimezoneOffset() / 60;
	$( "input[name='tz-offset']" ).val(currentTimeZoneOffsetInHours);
}		

function getRandom(arr, n) {
    var result = new Array(n),
        len = arr.length,
        taken = new Array(len);
    if (n > len)
        throw new RangeError("getRandom: more elements taken than available");
    while (n--) {
        var x = Math.floor(Math.random() * len);
        result[n] = arr[x in taken ? taken[x] : x];
        taken[x] = --len;
    }
    return result;
}
	

source = $('#logo').css('background-image').replace(/^url\(['"]?/,'').replace(/['"]?\)$/,'');
newSource = source + '?' + new Date().getTime();
newUrl = 'url(' + newSource + ')';
$('#logo').css('background-image', newUrl);
	    
$(document).ready(function() {


	$('#weekly').click(
		function() {
			$('#day-of-week').show();
			$('.dow').html('on ' + $('select[name="day-of-week"] option:selected').text());
		});
	
	$('#daily').click(
		function() {
			$('#day-of-week').hide();
			$('select[name="day-of-week"]').val(0);
			$('.dow').html('tomorrow');
		});
	
	


	$('.btn-frequency').click(function() {	
		if($(this).attr('id') == 'weekly') {
			$('input[name="frequency"]').val(1);
		} else if ($(this).attr('id') == 'daily') {
			$('input[name="frequency"]').val(2);
		} else {
			$('input[name="frequency"]').val(3);
		}
		
	
	});
	
	$("[type=checkbox]").on("click", function(){
	var id = $(this).attr('id');
    if ($(this).attr("checked")==undefined) { 
            $(this).attr("checked","checked");
            if(id == 'checkbox-twitter') {
            	$('input[name="my-tweets"]').val(1);
            } else if (id == 'checkbox-instagram') {
            	$('input[name="my-photos"]').val(1);
            } else if (id == 'checkbox-remixing') {
            	$('input[name="remixing"]').val(1);
            } else if (id == 'checkbox-zen') {
            	$('input[name="zen"]').val(1);
            } else if (id == 'checkbox-podcasts') {
            	$('input[name="podcasts"]').val(1);
            } else if (id == 'checkbox-voyeurism') {
            	$('input[name="voyeurism"]').val(1);
            } else if (id == 'checkbox-appendix-t') {
            	$('input[name="appendix-t"]').val(1);
            } else if (id == 'checkbox-appendix-i') {
            	$('input[name="appendix-i"]').val(1);
            } else if (id == 'checkbox-day-of-week'){
            	$('select[name="day-of-week"]').prop('disabled', true);
            	$('input[name="surprise-day"]').val(1);
            } else {
            	$('input[name="time-of-day"]').prop('disabled', true);
            	$('input[name="surprise-time"]').val(1);
            }
        } else {
           $(this).attr("checked",false);
           if(id == 'checkbox-twitter') {
            	$('input[name="my-tweets"]').val(-1);
            } else if (id == 'checkbox-instagram') {
            	$('input[name="my-photos"]').val(-1);
            } else if (id == 'checkbox-remixing') {
            	$('input[name="remixing"]').val(-1);
            } else if (id == 'checkbox-zen') {
            	$('input[name="zen"]').val(-1);
            } else if (id == 'checkbox-podcasts') {
            	$('input[name="podcasts"]').val(-1);
            } else if (id == 'checkbox-voyeurism') {
            	$('input[name="voyeurism"]').val(-1);
            } else if (id == 'checkbox-appendix-t') {
            	$('input[name="appendix-t"]').val(-1);
            } else if (id == 'checkbox-appendix-i') {
            	$('input[name="appendix-i"]').val(-1);
            } else if (id == 'checkbox-day-of-week'){
            	$('select[name="day-of-week"]').prop('disabled', false);
            	$('input[name="surprise-day"]').val(-1);
            } else {
            	$('input[name="time-of-day"]').prop('disabled', false);
            	$('input[name="surprise-time"]').val(-1);
            }
        }
	});  

	$('#twitter_pickforme').click(
		function() {
			var array = $('#twitter_usernames_string').html().split(',');
			var numElements = 10;
			if (array.length < 10) {
				numElements = array.length - 1;
			}
			var usernames = getRandom(array, numElements);
			$('#twitters').tokenfield('setTokens', usernames);
			return false;
	});
	
	
	
	
	$('#instagram_pickforme').click(
		function() {
			var array = $('#instagram_usernames_string').html().split(',');
			var numElements = 10;
			if (array.length < 10) {
				numElements = array.length - 1;
			}
			var usernames = getRandom(array, numElements);
			$('#instagrams').tokenfield('setTokens', usernames);
			return false;
	});
	
	$('.typeahead').change(
	function() {
		var num_tokens = 0;
		if ($(this).val().indexOf(',') !== -1) {
			var tokens = $(this).val().split(',');
			num_tokens = tokens.length;
		} else if ($(this).val() != '') {
			num_tokens = 1;
		}
		$(this).parents('.form-group').next().children('.num-remaining').children('.num').html(10-num_tokens);
		
		if (num_tokens==8) {
			$(this).parents('.form-group').next().children('.num-remaining').children('.p').html('people');
		}
		if (num_tokens==9) {
			$(this).parents('.form-group').next().children('.num-remaining').children('.p').html('person');
		}

		if (num_tokens==10) {
			$(this).parents('.form-group').next().children('.num-remaining').children('.p').html('people');
		}

	});
		
		

	$( 'select[name="day-of-week"]' ).change(function() {
	  	$('.dow').html($(this).children('option:selected').text());
	});
	 
	 
	  
	$( '#timepicker' ).change(function() {
	  	$('.tod').html($(this).val());
	});


	$( '#checkbox-day-of-week' ).click(function() {
		if($(this).attr("checked")==undefined) {
			$('.dow').html($('select[name="day-of-week"]').children('option:selected').text());
		} else { $('.dow').html('some day this week');
		}
	});

	$( '#checkbox-time-of-day' ).click(function() {
		if($(this).attr("checked")==undefined) {
			$('.tod').html($('#timepicker').val());
		} else {
			$('.tod').html('some time');
		}
		
	});	

	
});
