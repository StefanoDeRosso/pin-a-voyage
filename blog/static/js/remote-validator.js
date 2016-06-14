$(document).ready(function(){
	$("#user_form").validate({
             rules:
             {
                email:
                {
                    required: true,
                    email: true,
                    remote: {
						url: "/check_email/",
						type: "get",
					  },
                },
                first_name:
                {
                    required: true,
                    minlength: 3
                },
                second_name:
                {
                    required: true,
                    minlength: 3
                },
                password1:
                {
                    required: true,
                    minlength: 8
                },
             },
             messages:
             {
                 email:
                 {
                    remote: jQuery.validator.format("<ul style='margin: 0;'><li style='font-weight:100'><strong>{0}</strong> is already in use.</li></ul>")
                 },
             },
         });

    });
