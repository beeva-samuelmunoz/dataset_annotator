function annotator_bbox(canvas, msg){
	//Connection
	var url_api = '/api';
	var url_img = '/img';
	//App status
	var canvas = canvas;  // Where to draw
	var ctx = canvas.getContext("2d");
	var msg = msg;  //mesage to show
	var status = '';  //Drawing status
	//Data
	var img_id = "";  // Id of the img in the datset. path
	var imgb64 = "";  //Downloaded img in base64
	var bboxes = [];  //Annotated bboxes


	//
	// AJAX CALLS: RPC, IMGS
	//


	function rpc_get_new_img(callback){
		axios.post(url_api, {
			jsonrpc: '2.0',
			method: 'IMG.get_new_img',
			params: {},
			id: 1
	  })
	  .then(function (response) {
	    console.log(response);
			callback(response.data.result.img_id);
	  })
	  .catch(function (error) {
	    console.log(error);
	  });
	}

	function rpc_add_annotations(bboxes, callback){
		axios.post(url_api, {
			jsonrpc: '2.0',
			method: 'IMG.add_annotations',
			params: {
				img_id: img_id,
				bboxes: bboxes
			},
			id: 1
		})
		.then(function (response) {
			console.log(response);
			callback();
		})
		.catch(function (error) {
			console.log(error);
		});
	}

	function get_img(img_id, callback){
		axios.get( url_img+"/"+img_id, {responseType:"blob"})
		.then(function (response) {
			console.log(response);
			var reader = new window.FileReader();
			reader.readAsDataURL(response.data);
			reader.onload = function() {
				callback(reader.result);  //b64 img
			}
		})
		.catch(function (error) {
			console.log(error);
		});
	}

	//
	// CANVAS
	//
	function canvas_set_image(){
		var img = new Image();
		img.onload = function(){
			console.log("canvas draw");
			ctx.drawImage(img, 0, 0, img.width, img.height);
		};
		img.src = imgb64;
		canvas.width = img.width;
		canvas.height = img.height;
	}



	//
	// BUTTONS
	//

	function reset(){
		bboxes = [];
		status = '';
		canvas_set_image();
	}

	function skip(){
		bboxes = [];
		status = '';
		//Get new image
		rpc_get_new_img(function(new_img_id){
			img_id = new_img_id;
			console.log("FUNCTION: skip");
			console.log("img_id: "+img_id);
			// get image
			get_img(img_id, function(new_imgb64){
				imgb64 = new_imgb64;
				canvas_set_image();
			});
		});
	}

	function send(){
		rpc_add_annotations(bboxes, function(){
			skip();
		})
	}

	return {
		send: send,
		reset: reset,
		skip:	skip
	}
}
