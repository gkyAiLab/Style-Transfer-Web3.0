var CAMERA=function(){
//	$('button').click(function(){
//		var user = $('#inputUsername').val();
//		var pass = $('#inputPassword').val();
		$.ajax({
			url: '/camera',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
				var data=JSON.parse(response);
//				document.getElementById("demo").innerHTML = data.result;
				$("#demo").html('<img src='+ data.result +'>');
                CAMERA();
			},
			error: function(error){
				console.log(error);
			}
		});
	}
	CAMERA();
//});

document.getElementById("logo").src = "img/logo.png"






