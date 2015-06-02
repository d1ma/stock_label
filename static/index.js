// var source = 'local';
var source = 'domino';



$(document).ready(function(){
	//id = $.getUrlVars()["id"]
	//console.log(id)
	var request_params = {}
	if (source == 'local'){
		request_params = {url: '/json_index'}
	} else if (source == 'domino'){
		request_params = {
			url: "https://app.dominodatalab.com/v1/jayhack/NGB/endpoint",
			headers: {
				"Content-Type": "application/json",
				"X-Domino-Api-Key": "kWJay9sqsjoLEH0NCoMvGrC0k0SFbBIqUnlEVcKzCYhmeUUsC8JDf6J5qD5nftsQ"
			},
			data: {
				"parameters": [ {"query_type":"populate_dashboard", "query":{}} ]
			}
		}
	}

	$.ajax(request_params)
	.done(function( data_text ){
		data = JSON.parse(data_text)
		console.log(data);
		if (data["status"] == 'Succeeded'){
			for (var i in data["result"]){
				var e = data["result"][i];
				
				console.log(e);
				entry = "<tr><td>" + e.id + "</td><td>" + e.name + "</td><td>";
				entry = entry + e.date + "</td><td>" + e.confidence + "</td></tr>";
				$("#IndexTable > tbody:last").append(entry);
			}
		}
			
		// for (int i = 0; i < data.length; i++)
		// {s
		// 	var sheet = data.eq(i);
		// 	console.log()
		// 	var id = sheet["id"];
		// 	var name = sheet["name"];
		// 	$("#table_container").after("<tr></tr>")
		// }
	});
	
	// $.ajax({
	// 	url: "/json_index" + id
	// })
	// .done(function( data ){
	// 	for (int i = 0; i < data.length; i++)
	// 	{s
	// 		var sheet = data.eq(i);
	// 		console.log()
	// 		var id = sheet["id"];
	// 		var name = sheet["name"];
	// 		$("#table_container").after("<tr></tr>")
	// 	}
	// });
});