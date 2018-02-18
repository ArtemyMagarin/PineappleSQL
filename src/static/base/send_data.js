function getCSRFToken() {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, 10) == ('csrftoken' + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(10));
                break;
            }
        }
    }
    return cookieValue;
}

var submit = function(url) {
	q = $('#query').val();

	// $.ajax({
	//   type: 'POST',
	//   url: url,
	//   data: postedData,
	//   dataType: 'json',
	//   success: callback
	// });

	$.ajax({
		url: url,
		type: "POST",
		data: {
			'query': q,
			'csrfmiddlewaretoken': getCSRFToken(),
		},
	})
	.done((data)=>{
	
		if (data['is_passed']) {
			COUNT = 1;
			$('<div class="alert alert-success alert-dismissible fade show mt-2" role="alert">Верно!<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>').insertAfter($('#query'))
			table = '<table class="table"><thead><tr><th scope="col">#</th>'
			data['heads'].forEach(function(data) {
				table += ('<th scope="col">'+data+'</th>')
			})
			table += '</thead><tbody>'

			data['rows'].forEach(function(data) {
				table += '<tr><th scope="row">'+(COUNT++)+'</th>'
				data.forEach(function(data) {
					table += '<td>'+data+'</td>'
				})
				table += '</tr>'
			})
			table += ' </tbody></table>'

			$('#result').append(table)
		} else {
			$('<div class="alert alert-danger alert-dismissible fade show mt-2" role="alert">Запрос неверен<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>').insertAfter($('#query'))
		}
	})
}