var isMouseDown = false;
var currentMode = null;
var temp = null;
var active = null;
var activatedIDs = {};
var cellsToAdd = {};
var subclassColorIndex = 1;
var options = ["stats","json","line-item"];
var helpTabs = ["overview","adding","removing","editing","hotkeys"];
var outputJSON = [];
var objectBuild = {}

function clearMode(){
	currentMode = null;
	$(".select_toggle").removeClass("active");
}

function setMode(toggle_id){
	switch(toggle_id){
		case "nav-title":
			return "title";
		case "nav-locale":
			return "locale";
		case "nav-item":
			return "item";
		case "nav-price":
			return "price";
		case "nav-subclass":
			return "subclass";
		default:
			return null;
	}
}

function getCurrentClass(){
	if (currentMode != null)
		return currentMode;
	else
		return null;
}

function unhighlightAll(){
	for(key in activatedIDs){
		// if($("#"+activatedIDs[key]).hasClass("activated") && $("#"+activatedIDs[key]).hasClass("processedPrice")) $("#"+activatedIDs[key]).removeClass("activated");
		unhighlightAttributes(activatedIDs[key],false,false);
	}
	for(key in $())
	activatedIDs = {};
}

function resetRound(){
	currentMode = null;
	resetToggles(null);
	unhighlightAll();
	resetMarking('price');
	resetMarking('item');
	resetMarking('subclass1');
	resetMarking('subclass2');
	resetMarking('subclass3');
	resetMarking('locale');
	resetMarking('title');
	subclassColorIndex = 0;
}

function roundInProgress(){
	for(key in cellsToAdd){
		console.log(cellsToAdd[key]);
		if(cellsToAdd[key] > 0) return true;
	}

	return false;
}

function saveState(oldState){
	console.log("Save state called");
	console.log(oldState);
	switch (oldState){
		
		case "price":
			objectBuild.price = $(".price");
			cellsToAdd["price"] = $(".price").length;
			console.log("adding cells X cells to price:");
			console.log(cellsToAdd["price"]);
			return true;
		
		case "item":
			items = $(".item");
			objectBuild.item = items;
			cellsToAdd["item"] = $(".item").length;

		case "subclass":
			subclassColorIndex+=1;
			if (objectBuild.subclass === undefined){
				objectBuild.subclass = [];
			}
			subclasses = $(".new_subclass");
			$(".new_subclass").removeClass("new_subclass");
			subclasses_clean = []

			for (var i = 0; i < subclasses.length; i++)
			{
				sub = {}
				sub.loc = subclasses.get(i).id;
				sub.val = subclasses.get(i).innerHTML;
				subclasses_clean.push(sub);
			}
			if(subclasses_clean.length > 0) objectBuild.subclass.push(subclasses_clean);
			cellsToAdd["subclass"] = subclasses_clean.length;
			if(objectBuild.subclass.length > 1){
				var numSubclasses = 0;
				for(sub in objectBuild.subclass){
					numSubclasses += objectBuild.subclass.length;
				}
				cellsToAdd["subclass"] = numSubclasses;

			}

		case "locale":
			locale = $(".locale");
			objectBuild.locale = locale;
			cellsToAdd["locale"] = $(".locale").length;
	}
}

function resetToggles(currentstate){
	console.log("is this being reset");
	states = ["nav-price", "nav-item", "nav-subclass", "nav-locale",
			   "nav-title", "add"];
    for (state in states){
    	parent = $("#"+states[state]);
    	// .parent()
		parent.removeClass("disabled");
		parent.removeClass("active");
    }
}


function toggleOff(oldState){
	buttonMap = {"price":"nav-price", "item":"nav-item", "subclass":"nav-subclass", "locale":"nav-locale"}
	$("#"+buttonMap[oldState]).removeClass("active");
	// .parent().removeClass("active");
}

function processToggleClick(toggle_id){
	unhighlightAll();
	var isActive = $("#"+toggle_id).hasClass("active");
	// .parent().hasClass("active");
	var oldMode = currentMode;
			console.log("outside oldmode processToggle");

	if(oldMode){
		console.log("in oldmode processToggle");
		var result = saveState(oldMode);
		if (result) {
			toggleOff(oldMode);
			// switchToggles(oldMode);
		}
	}
	clearMode();
	if(!isActive){
		currentMode = setMode(toggle_id);
		$("#"+toggle_id).addClass("active");
		// .parent().addClass("active");

	}
}

function getTitle(){
	if ($(".title").length > 0){
		return $(".title")[0].innerHTML;
	}else{
		return null;
	}
}

function getLocale(){
	if ($(".title").length > 0){
		return  $(".title")[0].innerHTML;
	}else{
		return null;
	}
}

function getItem(){
	var items = $(".item");
	if (items.length > 0){
		return items[0].innerHTML;
	}else{
		return null;
	}
}

function getPrice(){
	var prices = $(".item");
	if (prices.length > 0){
		return prices[0].innerHTML;
	}else{
		return "n/a";
	}
}

function errorCheckElements(){
	errors = [];
	error = false;
	
	if(objectBuild.price == null || objectBuild.item == null){
		errors.push("Please choose at least one price and corresponding item");
		error = true;
	}
	else if (objectBuild.price.length != objectBuild.item.length && objectBuild.item.length != 1){
		console.log(objectBuild.price.length);
		console.log(objectBuild.item.length);
		errors.push("Please choose one corresponding item for each price chosen or one item for the entire set of prices");
		error = true; 
	}
	
	if(objectBuild.locale && objectBuild.locale.length > 1){
		errors.push("Please choose one locale per set of prices");
		error = true;
	}
	
	if(objectBuild.subclass && objectBuild.subclass.length > 0){
		console.log(objectBuild.subclass);
		console.log("object build subclass length:" + objectBuild.subclass.length)
		console.log("objectBuild.subclass");
		var index = 0;
		for(subsub in objectBuild.subclass){
			console.log("object build subclass subsub length:" + objectBuild.subclass[subsub].length)

			if (objectBuild.subclass[subsub].length != 1 && objectBuild.subclass[subsub].length != objectBuild.price.length){
				errors.push("Please choose one corresponding subclass element for each price chosen or one subclass for the entire set of prices");
				error = true;
				break;
			}

		}
	}

	if(error){
		resetRound();
		currentMode = null;
		resetToggles(null);
		alert(errors.join('\n'));
		objectBuild = {}
		return true;
	}

	return false;
}



function addElements(){


	if(errorCheckElements()) return;	


	if (objectBuild.title === undefined){
		objectBuild.title = null;
	}
	if (objectBuild.locale === undefined){
		objectBuild.locale = null;
	}
	if (objectBuild.subclass === undefined){
		objectBuild.subclass = [];
	}

	for (var price_i = 0; price_i < objectBuild.price.length; price_i++){
		if(objectBuild.price.eq(price_i).hasClass("processedPrice")) continue; 
		console.log('YA');
		var subclass_list = [];
		for (var subclass_i = 0; subclass_i < objectBuild.subclass.length; subclass_i++){
			var s = objectBuild.subclass[subclass_i];
			// if (s.length == 1){
			// 	console.log("subclass_list.push(s): " + s)
			// 	subclass_list.push(s);
			// }else{
			if(s.length==1){
				subclass_list.push(s[0]);
			} else {
				console.log("subclass_list.push(s[price_i]);")
				console.log(s[price_i]);
				subclass_list.push(s[price_i]);
			}
			// }
		}

		var obj = {};
		if (objectBuild.locale != null){
			obj.locale = {}
			obj.locale.val = objectBuild.locale.html();
			obj.locale.loc = objectBuild.locale.attr('id');
		}else{
			obj.locale = null;
		}
		obj.price = {};
		obj.price.val = objectBuild.price[price_i].innerHTML;
		obj.price.loc = objectBuild.price[price_i].id;
		obj.subclass = subclass_list; 

		if (objectBuild.item.length == 1){
			obj.item = {}
			obj.item.val = objectBuild.item[0].innerHTML;
			obj.item.loc = objectBuild.item[0].id;
		}
		else{
			obj.item = {}
			obj.item.val = objectBuild.item[price_i].innerHTML;
			obj.item.loc = objectBuild.item[price_i].id;
		}
		console.log("value of obj is:");
		console.log(obj);
		console.log(outputJSON);
		outputJSON.push(obj);
	}
	objectBuild = {};
}

function resetMarking(markingName){
	var items = $("." + markingName);
	items.removeClass(markingName);
}

function resetMarkings(){
	prices = $('.price');
	prices.addClass('processedPrice');
	resetRound();
}

function sendAjax(sheet_id, data){
	console.log("sending: " + data);

	$.ajax({
	    type : "POST",
	    url : "/upload/" + sheet_id,
	    data: JSON.stringify(data),
	    contentType: 'application/json',
	    success: function(result) {
	        console.log("response: " + result);
	    }
	});
}

function sendStagingAjax(sheet_id, stage_status){

	$.ajax({
	    type : "GET",
	    url : "/stage/" + sheet_id + "/" + stage_status,
	    success: function(result) {
	        console.log("response: " + result);
	    }
	});

}

function processAdd(){
	addElements();
	displayJSON();
	resetMarkings();
	resetToggles(currentMode);
	currentMode = null;

}

function saveAjax(){
	var sheet_id = $("#sheet_id").html();
	console.log("sending ajax to for sheet " + sheet_id);
	data = {};
	data["labels"] = outputJSON;
	data["vendor"] = $("#vendor_list").val();
	sendAjax(sheet_id, data);
}

function findJSONObject(id){
	for (var key in outputJSON){
		if(outputJSON[key] && outputJSON[key].price.loc == id){
			return outputJSON[key];
		}
	}


}

function unhighlightAttributes(id, active, toDelete){
	if(!active){
		var object = findJSONObject(id);
		for(key in object){
			if(key == 'locale' && object[key]){
				$("#"+object[key].loc).removeClass('activeLocale');

			} else if (key == 'item' && object[key]){
				$("#"+object[key].loc).removeClass('activeItem');

			} else if (key == 'price' && object[key]){
				// $("#j"+object[key].loc).removeClass('lineItemActive');
				// $("#j"+object[key].loc).removeClass('activePrice');
				$("#j"+object[key].loc).removeClass();
				if(toDelete){
					$("#"+object[key].loc).removeClass();
					$("#"+object[key].loc).addClass('cell');

				} else {
					// $("#"+object[key].loc).removeClass('processedPrice'))
					$("#"+object[key].loc).removeClass();

					$("#"+object[key].loc).addClass('cell');

					$("#"+object[key].loc).addClass('processedPrice');
					// $("#"+object[key].loc).removeClass('activePrice');

				}
			} else if (key == 'subclass' && object[key][0] && object[key].length > 0){
			// for(subclass in object[key]){
			// 	console.log('highlightSubclass');
				for(sub = 0; sub < object["subclass"].length; sub++){
					//$("#" + object[key][sub].loc).removeClass('activeSubclass');
					//$("#j" + object[key][sub].loc).removeClass('activeSubclass');
					$("#" + object[key][sub].loc).removeClass();
					$("#j" + object[key][sub].loc).removeClass();
					$("#" + object[key][sub].loc).addClass('cell');
				}
			}
		}
	}

}

function highlightAttributes(id){
	var object = findJSONObject(id);
	for(key in object){
		if(key == 'locale' && object[key]){
			$("#"+object[key].loc).addClass('activeLocale');

		} else if (key == 'item' && object[key]){
			$("#"+object[key].loc).addClass('activeItem');

		} else if (key == 'price' && object[key]){
			$("#"+object[key].loc).removeClass('processedPrice');
			$("#"+object[key].loc).addClass('activePrice');
			$("#j"+object[key].loc).addClass('activePrice');

		} else if (key == 'subclass' && object[key][0] && object[key].length > 0){
			// for(subclass in object[key]){
			// 	console.log('highlightSubclass');
			for(sub = 0; sub < object["subclass"].length; sub++){
				// console.log(object[key][sub][0]);
				$("#" + object[key][sub].loc).addClass('activeSubclass');
			}
		}
		
	}
}


function cleanHTML(elemID){
	var h = $(elemID).html();
	
	var s = h.replace(/\\\"/g,'\"');
	s = s.trim();
	if (s.charAt(0)=='\"') s=s.substring(1,s.length - 1);
	if (s.charAt(s.length - 1)=='\"') s=s.substring(0,s.length -1);
	return s;
}

function initializeJSONCells(){
	try{
		html = cleanHTML('#line-item');
		console.log("html (initializeJSONCells):");
		$("#line-item").text(html);
		outputJSON = JSON.parse(html);
		
			for (key in outputJSON){
				if(outputJSON[key] && outputJSON[key].price){
					$("#"+outputJSON[key].price.loc).addClass('processedPrice');
				}
			}
		
		displayJSON();
		if(!outputJSON) outputJSON = [];
	} catch(err){
		console.log("Error parsing JSON");
	}
}

function displayJSON(){
	$("#json").empty();
	var JSONdiv = document.getElementById("json");
	for(key in outputJSON){
		var p = document.createElement("p");
		lineItem = outputJSON[key];
		var string = "Item: " + lineItem["item"].val + "<br>Price: " + 
			lineItem["price"].val;
		if(lineItem["subclass"].length > 0 && lineItem["subclass"][0]){
			string = string.concat("<br>Subclass: ");
			for(sub = 0; sub < lineItem["subclass"].length; sub++){
				string = string.concat(lineItem["subclass"][sub].val);
			}
		}
		if(lineItem["locale"] && lineItem["locale"].val) string = string.concat("<br>Locale: " + lineItem["locale"].val);
		string = string.concat("<br>[Row_Col]: " + lineItem["price"].loc);
		p.innerHTML = string;
		p.setAttribute("id","j"+lineItem["price"].loc);
		if($("#"+outputJSON[key].price.loc).hasClass('activated') || $("#"+outputJSON[key].price.loc).hasClass('selected')){
			console.log("yay highlighted");
			p.setAttribute("class","lineItemActive");
		}
		JSONdiv.appendChild(p);
	}
	if(outputJSON){
		var vendor = $("#vendor").html();
        $("#line-item").html("<p>"+JSON.stringify(outputJSON)+"</p>");
        $("#stats").html("<p id='vendor'>" + vendor +"</p><p><b>Items Selected:</b> " + outputJSON.length + "</p>");
 }

};

function deleteObjects(){
	objectsToDelete = document.getElementsByClassName("activated");
    //console.log(objectsToDelete);
    for(object in objectsToDelete){

    	var objID = objectsToDelete[object].id;
    	if(objID){
    		console.log(objID)
			for (var key=0; key < outputJSON.length; key++){
				if(outputJSON[key] && outputJSON[key].price.loc == objID){
					unhighlightAttributes(objID,false, true);
					outputJSON.splice(key, 1);
					key--;
					//break;
						// delete allObjects[key];
				}
			}
    	}
   	}
   	displayJSON();
   	var sheet_id = $("#sheet_id").html();
	console.log("sending ajax to for sheet " + sheet_id);
	saveAjax();
}

function switchOption(id){
	for(key in options){
		$("#"+options[key]).addClass("invisible");
		$("#options-"+options[key]).removeClass("active");
	}
	$("#"+id).removeClass("invisible");
	$("#options-"+id).addClass("active");

}

function switchHelpTabs(id){
	for(key in helpTabs){
		$("#"+helpTabs[key]).addClass("invisible");
		$("#help-"+helpTabs[key]).removeClass("active");
	}
	$("#"+id).removeClass("invisible");
	$("#help-"+id).addClass("active");

}

function adjustHeight(){
	adjustFactor = 0.8;
	if ($(window).height() < 400) adjustFactor = 0.65;
	height = $(window).height()*adjustFactor;
	console.log(height);
	$("#spreadsheet_container").height(height);
	$(".options").height(height);
}



$(document).ready(function(){
	console.log("Loaded");
	adjustHeight();
  	initializeJSONCells();
  	console.log("displayed");
  	resetRound();

  	$('table.paginated').each(function() {
	    var currentPage = 0;
	    var numPerPage = 50;
	    var $table = $(this);
	    $table.bind('repaginate', function() {
	        $table.find('tbody tr').hide().slice(currentPage * numPerPage, (currentPage + 1) * numPerPage).show();
	    });
	    $table.trigger('repaginate');
	    var numRows = $table.find('tbody tr').length;
	    var numPages = Math.ceil(numRows / numPerPage);
	    var $pager = $('<div class="pager"></div>');
	    for (var page = 0; page < numPages; page++) {
	        $('<span class="page-number"></span>').text(page + 1).bind('click', {
	            newPage: page
	        }, function(event) {
	            currentPage = event.data['newPage'];
	            $table.trigger('repaginate');
	            $(this).addClass('active_page').siblings().removeClass('active_page');
	        }).appendTo($pager).addClass('clickable');
	    }
	    $pager.insertAfter($table).find('span.page-number:first').addClass('active_page');
	})

  	
  	$(window).resize(function(){
  		adjustHeight();
  	}) 

  	$(".cell").mousedown(function () {
      isMouseDown = true;

      	$(this).toggleClass(getCurrentClass());
     	if (getCurrentClass() == "subclass"){
        	$(this).toggleClass(getCurrentClass());
        	$(this).toggleClass(getCurrentClass() + subclassColorIndex );
        	$(this).toggleClass("new_subclass");
        } else if($(this).hasClass("selected")){
    		highlightAttributes($(this).attr("id"));
    		// active = $(this).attr("id");
    		$("#find").text(String("Search: "+$(this).attr("id")));
    		$("#find").attr("href", "#j" + $(this).attr("id"));

    		$(this).addClass("activated");
    		activatedIDs[$(this).attr("id")] = $(this).attr("id");
      	} else if ($(this).hasClass("activated")){
      	 	unhighlightAttributes($(this).attr("id"), false, false);
      	 	$(this).removeClass("activated");
      	 	delete activatedIDs[$(this).attr("id")];

      	} else if ( $(this).hasClass("processedPrice") && getCurrentClass()) {
      		isMouseDown = false;
      		$(this).toggleClass(getCurrentClass());
      		alert("This cell has already been listed as a price. If you wish to edit it, delete it and add it once more.");
      	}
     return false; // prevent text selection

    })
    .mouseover(function () {
      if (isMouseDown) {
      	$(this).toggleClass(getCurrentClass());
        if (getCurrentClass() == "subclass"){
        	$(this).toggleClass(getCurrentClass());
        	$(this).toggleClass(getCurrentClass() + subclassColorIndex );
        	$(this).toggleClass("new_subclass");
        } else if($(this).hasClass("processedPrice") && getCurrentClass() == null 
        		&& !$(this).hasClass("activated")){
    		highlightAttributes($(this).attr("id"));
      		$(this).addClass("activated");
    		activatedIDs[$(this).attr("id")] = $(this).attr("id");

      		$("#find").text(String("Search: "+$(this).attr("id")));
      		$("#find").attr("href", "#j" + $(this).attr("id"));
      	} else if($(this).hasClass("activated")){
      		$(this).removeClass("activated");
      	 	unhighlightAttributes($(this).attr("id"), false, false);
      		delete activatedIDs[$(this).attr("id")];

      	}
      } else if($(this).hasClass("processedPrice") && getCurrentClass() == null && !roundInProgress()){
      		console.log("Round is not in progress");
      	// && cellsToAdd == 0 ){
      		$(this).addClass("selected");
      		highlightAttributes($(this).attr("id"));
      }
    })
    .mouseout(function(){
    	if($(this).hasClass("selected")){
    		$(this).removeClass("selected");
    		unhighlightAttributes($(this).attr("id"), $(this).hasClass("activated"), false);
    	}
    });

    $(document).keypress(function(e) {
    	if (e.which == 97) { /* pressed a */
    		processToggleClick("nav-price");
    		console.log("Toggling from e which");
    	} else if (e.which == 115) { /* pressed s */
    		processToggleClick("nav-item");
    	} else if (e.which == 100) { /* pressed d */
    		processToggleClick("nav-locale");
    	} else if (e.which == 102) { /* pressed f */
    		processToggleClick("nav-subclass");
    	} 
    	else if (e.which == 120) { /* pressed x */
    		processToggleClick(getCurrentClass());
    		processAdd();
    		cellsToAdd = {};
    		saveAjax();

    	} else if (e.which == 116){
    		deleteObjects();
    		saveAjax();

    	}
    	console.log("key pressed: " + e.which);
	});

    $('#nav-price').on("click",function(){
		processToggleClick("nav-price");
		return false;
	});

	$('#nav-item').on("click",function(){
		processToggleClick("nav-item");
		return false;
	});

	$('#nav-locale').on("click",function(){
		processToggleClick("nav-locale");
		return false;
	});

	$('#nav-subclass').on("click",function(){
		processToggleClick("nav-subclass");
		return false;
	});


	$("#add").on("click", function(){
    	processToggleClick(getCurrentClass());
		processAdd();
		cellsToAdd = {};
		saveAjax();
		return false; // prevent default
	});

	$("#reset").on("click", function(){
		resetRound();
		currentMode = null;
		resetToggles(null);
		return false; // prevent default
	});

	$(".navlink").on("click", function(){
		return false;
	});

	$("#delete").on("click",function(){
		deleteObjects();
		saveAjax();
		return false;
	});

	$("#options-stats").on("click",function(){
		switchOption("stats");
	});

	$("#options-json").on("click",function(){
		switchOption("json");
	});

	$("#options-line-item").on("click",function(){
		switchOption("line-item");
	});

	$("#help-overview").on("click",function(){
		switchHelpTabs("overview");
	})

	$("#help-adding").on("click",function(){
		switchHelpTabs("adding");
	})

	$("#help-removing").on("click",function(){
		switchHelpTabs("removing");
	})

	$("#help-editing").on("click",function(){
		switchHelpTabs("editing");
	})


	$("#help-hotkeys").on("click",function(){
		switchHelpTabs("hotkeys");
	})

	$("#delete_all").on("click",function(){
		var cleanAll = confirm("Are you sure you wish to delete all the labeled data?");
		if(cleanAll == true){
			$(".processedPrice").each(function(){
				$(this).addClass("activated");
			});
			deleteObjects();
		}
		return false;
	})

	$("#new-vendor").on("click",function(){
        var vendorToAdd = prompt("What is the name of the vendor you would like to add?", "e.g. Twin Brothers");
        if(vendorToAdd != null){
            $("#vendor_list").append("<option value='"+vendorToAdd
            +"' selected='selected'>"+vendorToAdd+"</option>");
        }
        saveAjax();

    })

    $("#vendor_list").on("change",function(){
    	saveAjax();
    })

    $(".staged").on("click",function(){

    	console.log("hell");
    	console.log($(this.id));

    	if ( $(this).hasClass('btn')){
			var sheet_id = $("#sheet_id").html();
    	} else {
    		var sheet_id = $(this).attr("sheet");
    		$(this).removeClass("label-success");
    		$(this).addClass("label-danger");
	    	$(this).text("Not Staged");

    	}

    	console.log(sheet_id);

    	$(this).removeClass("staged");
    	$(this).addClass("unstaged");

    	sendStagingAjax(sheet_id,"no");

    	window.location.reload();

    })

    $(".unstaged").on("click",function(){
    	
    	
    	if( $(this).hasClass('btn')){
			var sheet_id = $("#sheet_id").html();
    	} else {
    		var sheet_id = $(this).attr("sheet");
    		$(this).removeClass("label-danger");
    		$(this).addClass("label-success");
    		$(this).text("Staged");

    	}
    	

    	$(this).removeClass("unstaged");
    	$(this).addClass("staged");
    	window.location.reload();
    	sendStagingAjax(sheet_id,"yes");

    })


    $("#pull").on("click", function(){

    	$.ajax({
	   	 	type : "GET",
	    	url : "/pull",
	    	success: function(result) {
	        	alert(result);
	    	}
		});
    })

});

$(document)
.mouseup(function () {
  isMouseDown = false;
});

