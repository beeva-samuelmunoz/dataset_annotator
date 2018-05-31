// Listen to "Too many Zooz" !!

function annotator_bbox(canvas, msg){
	//Connection
	var url_api = '/api';
	var url_img = '/img';
	//App status
	var canvas = canvas;  // Where to draw
	var ctx = canvas.getContext("2d");
	var canvas_offset = canvas.getBoundingClientRect();

	var msg = msg;  //mesage to show
	var canvas_click = {x:0, y:0} // when drawing on canvas, initial position.


	//Data
	var img_id = "";  // Id of the img in the datset. path
	var img = "";  // HTML img element to copy on canvas
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
			// console.log(response);
			callback();
		})
		.catch(function (error) {
			console.log(error);
		});
	}

	function get_img(img_id, callback){
		img = new Image();
		img.onload = function(){
			callback();
		};
		img.src = url_img+"/"+img_id;

	}

	//
	// CANVAS
	//

	function canvas_update(){
		// Background
		canvas.width = img.width;
		canvas.height = img.height;
		ctx.drawImage(img, 0, 0);
		// BBoxes
		for (bbox of bboxes) {
			ctx.beginPath();
			ctx.lineWidth="2";
			ctx.strokeStyle="magenta";
			ctx.rect(bbox.x, bbox.y, bbox.width, bbox.height);
			ctx.stroke();
		}
	}

	function canvas_press(e){
		canvas_click.x = e.pageX-canvas_offset.left;
		canvas_click.y = e.pageY-canvas_offset.top;
		canvas.addEventListener('mousemove', canvas_move);
	}

	function canvas_release(e){
		canvas.removeEventListener('mousemove', canvas_move);
		//Add bbox
		bboxes.push(points2bbox(
			canvas_click.x, canvas_click.y,
			e.pageX-canvas_offset.left, e.pageY-canvas_offset.top)
		);
		canvas_update();
	}

	function canvas_move(e){
		canvas_update();
		//Draw current bbox
		var bbox = points2bbox(
			canvas_click.x, canvas_click.y,
			e.pageX-canvas_offset.left, e.pageY-canvas_offset.top
		);
		ctx.beginPath();
		ctx.lineWidth="2";
		ctx.strokeStyle="yellow";
		ctx.rect(bbox.x, bbox.y, bbox.width, bbox.height);
		ctx.stroke();

	}

	function points2bbox(x1,y1,x2,y2){
		var xmin,xmax;
		x1<x2? (xmin=x1, xmax=x2): (xmin=x2, xmax=x1)
		y1<y2? (ymin=y1, ymax=y2): (ymin=y2, ymax=y1)
		return {
			x: xmin,
			y: ymin,
			width: xmax-xmin,
			height: ymax-ymin
		}
	}

	//Listeners
	canvas.addEventListener('mousedown', canvas_press);
	canvas.addEventListener('mouseup', canvas_release);




	//
	// BUTTONS
	//

	function reset(){
		console.log("FUNCTION: reset");
		bboxes = [];
		status = '';
		if (img_id!==null){
			canvas_update();
		}
	}

	function skip(){
		console.log("FUNCTION: skip");
		bboxes = [];
		status = '';
		img_id = '';
		//Get new image
		rpc_get_new_img(function(new_img_id){
			img_id = new_img_id;
			console.log("img_id: "+img_id);
			// get image
			if (img_id == null) {
				canvas.width = 0;
				canvas.height = 0;
				msg.innerText = "No more images";
			} else{
				get_img(img_id, function(new_imgb64){
					// imgb64 = new_imgb64;
					canvas_update();
				});
			}
		});
	}

	function send(){
		console.log("FUNCTION: send");
		console.log("bboxes: ");
		console.log(bboxes);
		if (img_id!==null){
			rpc_add_annotations(bboxes, function(){
				skip();
			});
		}
	}

	return {
		send: send,
		reset: reset,
		skip:	skip
	}
}
