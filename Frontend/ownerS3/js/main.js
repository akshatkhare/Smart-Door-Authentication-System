
// WP-1
function submitToVisitorForm(e) {
    var faceid;
    var fileName;
    //faceid = 1234;
    var link = window.location.href;
    if (link) {
    console.log(link)
    link = link.split('?')[1];
    var arr = link.split('&');
    for (var i = 0; i < arr.length; i++) {
        var a = arr[i].split('=');
        if (a[0] == "faceId") {
            faceid = a[1];
        }
        if (a[0] == "fileName") {
            fileName = a[1];
        }
    }
    }
	console.log(document.getElementById("name-input").value);
	console.log(document.getElementById("phone-input").value);
    console.log(faceid);
	var apigClient = apigClientFactory.newClient();
	var params = {};

	var body = {
        'message': {
			'name-input':document.getElementById("name-input").value,
			'phone-input':document.getElementById("phone-input").value,
            'face-id':String(faceid),
            'file-name':String(fileName)
		}
    }
	var additionalParams = {};
    apigClient.rootPost(params, body, additionalParams)
    .then(function(result){
        console.log(result);
	alert(result["data"]["body"]);
    }).catch( function(result){
        //This is where you would put an error callback
        console.log(result)
		
    });
}

