function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

Parsley.addAsyncValidator(
  'emailCheck', function (xhr) {
       var email = $('#email').parsley();
       var response = xhr.responseText;
	   var jsonResponse = JSON.parse(response);
	   var jsonResponseText = jsonResponse["response"];
	   
       if(jsonResponseText == 'This E-mail is ok.')
           return true;
       if(jsonResponseText == '404')
		   return false;
  }, '/email_check/'
);


$(document).ready(function() {
    $("#login-form").submit(function(e) {
        var csrftoken = getCookie('csrftoken');
        var password = $('#login-password').val();
        var email = $('#login-email').val();
        var res = e.responseText;

        $.ajax({
            url: "/password_check/",
            type: "POST",
            dataType: "json",
            data : {
                csrfmiddlewaretoken: csrftoken,
                password: password,
                email: email,
                result: res
            },
            success: function(result) {
                if(result.response == ""){
					document.getElementById("login-form").submit();
				} else {
					document.getElementById("login-error").innerHTML = result.response;
				}
            }
        });
        return false;
    });
});

$(document).ready(function(){
	$("#subscribe_btn").click(function(){
		$("#subscribe_modal").modal();
	});
});

$(document).ready(function(){
	$("#login_btn").click(function(){
		$("#login_modal").modal();
	});
});

$( document ).ready( function(){
	setMaxWidth();
	$( window ).bind( "resize", setMaxWidth ); //Remove this if it's not needed. It will react when window changes size.

	function setMaxWidth() {
	$( "img" ).css( "maxWidth", ( $( window ).width() * 0.7 | 0 ) + "px" );
	}

});

$(document).ready(function(){
    $('a').tooltip({placement: "bottom"});   
});

window.fbAsyncInit = function() {
	FB.init({
	  appId      : '1045362668884516',
	  xfbml      : true,
	  version    : 'v2.6'
	});
};

(function(d, s, id){
     var js, fjs = d.getElementsByTagName(s)[0];
     if (d.getElementById(id)) {return;}
     js = d.createElement(s); js.id = id;
     js.src = "//connect.facebook.net/en_US/sdk.js";
     fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

if (window.location.hash == '#_=_') {
      window.location.hash = '';
   }

