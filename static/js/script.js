var boxes = [];
var lines = [];
var turn = true;
var you = 0;
var you2 = 0;
var comp = 0;
var comp2 = 0;
var comp3 = 0;
var mode = "pvp";
var m = 0; //kolone
var n = 0; //redovi
var d = 0; //dubina

/*$("body").bind("ajaxSend", function(elm, xhr, s){
	if (s.type == "POST") {
	   xhr.setRequestHeader('X-CSRF-Token', csrf_token);
	}
 }); */

function load(m, n, mode) {
	boxes = [];
	lines = [];
	turn = true;
	switch (mode) {
		case "pvp": {
			you = 0;
			you2 = 0;
			$("#turn").text("Turn :" + "Player1");
			$(".player2").text("P1: " + you);
			$(".player1").text(you2 + " : P2");
		};
			break;
		case "pvc1": {
			you = 0;
			comp = 0;
			$("#turn").text("Turn :" + "You");
			$(".player2").text("You : " + you);
			$(".player1").text(comp + " : Comp");
		};
			break;
		case "pvc2": {
			you = 0;
			comp2 = 0;
			$("#turn").text("Turn :" + "You");
			$(".player2").text("You : " + you);
			$(".player1").text(comp2 + " : Comp");
		};
			break;
		case "pvc3": {
			you = 0;
			comp3 = 0;
			$("#turn").text("Turn :" + "You");
			$(".player2").text("You : " + you);
			$(".player1").text(comp3 + " : Comp");
		};
			break;
	}




	var offset = 70;

	var sx = window.innerWidth / 2 - (m * offset) / 2,
		sy = offset * 4;

	var html = "";

	html += `<div class="moves" id="pisac" style="z-index=${ 100}; left:85%; top:20%">
	<h5 style="text-align:center;color:white;text-decoration:underline;margin-top:5px;margin-botttom:20px;">Game Moves:</h5></div>`;
	$("#app").html(html);
	var c = 0; //broj boxa
	for (var i = 0; i < m; i++) {
		for (var j = 0; j < n; j++) {
			var x = sx + i * offset,
				y = sy + j * offset;

			if (j == 0) {
				html += `
				<div class="box" data-id="${c}" style="z-index=${i - 1}; left:${x + 2.5}px; top:${y + 2.5}px"></div>
				<div class="dot" style="z-index=${i}; left:${x - 5}px; top:${y - 5}px" data-box="${c}"></div>
				<div class="line lineh" data-line-1="${c}" data-line-2="${-m}" style="z-index=${i}; left:${x}px; top:${y}px" data-active="false"></div>
				<div class="line linev" data-line-1="${c}" data-line-2="${c - n}" style="z-index=${i}; left:${x}px; top:${y}px" data-active="false"></div>

				`;
				var pairh = c +", " + (-m);
				var pairv = c +", " + (c-n);

				lines.push(pairh);
				lines.push(pairv);
				boxes.push(0);
				c++;
			}
			else {
				//u svesci imas kako si smislio brojanje.
				html += `
				<div class="box" data-id="${c}" style="z-index=${i - 1}; left:${x + 2.5}px; top:${y + 2.5}px"></div>
				<div class="dot" style="z-index=${i}; left:${x - 5}px; top:${y - 5}px" data-box="${c}"></div>
				<div class="line lineh" data-line-1="${c}" data-line-2="${c - 1}" style="z-index=${i}; left:${x}px; top:${y}px" data-active="false"></div>
				<div class="line linev" data-line-1="${c}" data-line-2="${c - n}" style="z-index=${i}; left:${x}px; top:${y}px" data-active="false"></div>

				`;
				var pairh = c +", " + (c-1);
				var pairv = c +", " + (c-n);

				lines.push(pairh);
				lines.push(pairv);
				boxes.push(0);
				c++;
			}


		}
	}
	//desna strana
	for (var i = 0; i < n; i++) {
		var x = sx + m * offset,
			y = sy + i * offset;
		var z = (m-1) * n + i;
		console.log(z);
		html += `
				<div class="dot" data-box="${z}" style="z-index=${i}; left:${x - 5}px; top:${y - 5}px" ></div>
				<div class="line linev" data-line-1="${z}" data-line-2="${-m}" style="z-index=${i}; left:${x}px; top:${y}px" data-active="false"></div>
				`;

				var pairv = z +", " + (-m);
				lines.push(pairv);
	}
	//zadnji red
	for (var i = 0; i < m; i++) {
		var x = sx + i * offset,
			y = sy + n * offset;
		var z = (Number(n) - 1) + i * Number(n);
		html += `
				<div class="dot" style="z-index=${i}; left:${x - 5}px; top:${y - 5}px" data-box="${z}"></div>
				<div class="line lineh" data-line-1="${z}" data-line-2="${-m}" style="z-index=${i}; left:${x}px; top:${y}px" data-active="false"></div>
				`;

				var pairh = z +", " + (-m);


				lines.push(pairh);

	}
	//zadnja tacka
	html += `<div class="dot" data-box="${c - 1}" style="z-index=${i}; left:${sx + m * offset - 5}px; top:${sy + n * offset - 5}px" ></div>`
	$("#app").html(html);
	console.log(lines.toString());
	console.log(boxes.toString());
	applyEvents(mode);
}




function applyEvents(mode) {

	$("div.line").unbind('click').bind('click', function () {

		var id1 = parseInt($(this).attr("data-line-1"));
		var id2 = parseInt($(this).attr("data-line-2"));

		if (checkValid(this) && turn) {
			var a = false, b = false;
            if (Done()==true){
			$(".moves").append("<p>GAME OVER!</p>");
			return;}
			else {
			if (id1 >= 0) var a = addValue(id1);
			if (id2 >= 0) var b = addValue(id2);
			$(".moves").append("<p> " + $("#turn").text()+ " // Move: "+ id1 +", "+id2+ " .</p></br>");
			$(this).addClass("line-active");
			$(this).attr("data-active", "true");

			switch (mode) {
				case "pvp": {
					if (a === false && b === false) {
						turn = false;
						$("#turn").text("Turn :" + "Player2");
					}
				};
					break;
				case "pvc1": {
					if (a === false && b === false) {
						$("#turn").html("Turn :" + "Comp-Easy");
						setTimeout(function(){computer("pvc1")},100);
					}
				};
					break;
				case "pvc2": {
					if (a === false && b === false) {
						$("#turn").text("Turn :" + "Comp-Medium");
						setTimeout(function(){computer2("pvc2")},100);
					}
				};
					break;
				case "pvc3": {
					if (a === false && b === false) {
						$("#turn").text("Turn :" + "Comp-Hard");
						setTimeout(function(){computer3("pvc3")},100);
					}
				};
					break;
				}

		} }
		if(checkValid(this) && !turn && mode=="pvp") {


			 var id1 = parseInt($(this).attr("data-line-1"));
			 var id2 = parseInt($(this).attr("data-line-2"));


			var a = false, b = false;

			if (id1 >= 0) var a = addValue(id1);
			if (id2 >= 0) var b = addValue(id2);
			$(this).addClass("line-active");
			$(this).attr("data-active", "true");
			if (Done()==true){
			$(".moves").append("<p>GAME OVER!</p>");
			return;}
			else {
            $(".moves").append("<p> " + $("#turn").text()+ " // Move: "+ id1 +", "+id2+ " .</p></br>");
			if (a === true || b === true) {
				turn = false;
				$("#turn").text("Turn :" + "Player2");
			} else {
				turn = true;
				$("#turn").text("Turn :" + "Player1");
			} }
		}
	});
}



	function addValue(id) {
		boxes[id]++;

		if (boxes[id] == 4) {
			acquire(id);
			return true;
		}
		return false;
	}

	function acquire(id) {

		var color;

		switch (mode) {
			case "pvp": {
				if (turn) {
					color = "url('/static/orange.jpg')";
					you++;
				} else {

					color = "url('/static/green.jpg')";
					you2++;
				}
				$("div.box[data-id='" + id + "']").css("background-image", color);
		boxes[id] = 4;
		//console.log(boxes.toString());

		$(".player2").text("P1 : " + you);
		$(".player1").text(you2 + " : P2");

		var full = true;
		for (var i = boxes.length - 1; i >= 0; i--) {
			if (boxes[i] != 4) {
				full = false;
				break;
			}
		}

		if (full) {

			if (you>you2) $("#turn").html("Player 1 is the winner <br/> Play again?");
				else if (you<you2) $("#turn").html("Player 2 is the winner"  + "<br/>" + "Play again?");
				else if(you == you2)  $("#turn").html("It's a tie. Both won!" + "<br/>" + "Play again?");

				if (you>you2) alert(" Player 1 won!");
				else if (you<you2) alert("Player 2 won!")
				else if(you == you2)  alert("It's a tie!");
		}
			};
				break;
			case "pvc1": {
				if (turn) {
					color = "url('/static/orange2.jpg')";
					you++;
				} else {

					color = "url('/static/green2.jpg')";
					comp++;
				}
				$("div.box[data-id='" + id + "']").css("background-image", color);
		boxes[id] = 4;
		console.log(boxes);
		//console.log(boxes.toString());

		$(".player2").text("You : " + you);
		$(".player1").text(comp + " : Comp");

		var full = true;
		for (var i = boxes.length - 1; i >= 0; i--) {
			if (boxes[i] !== 4) {
				full = false;
				break;
			}
		}

		if (full){
				if (you>comp) $("#turn").html("You are the winner. Play again?");
				else if (you<comp) $("#turn").html("Computer is the winner. Play again?");
				else if(you == comp)  $("#turn").html("It's a tie. Both won! Play again?");

				if (you>comp) alert("You are the winner!");
				else if (you<comp) alert("Computer is the winner!")
				else if(you == comp)  alert("It's a tie!");

		}
				//i ostalo odozgo
			};
				break;
			case "pvc2": {
				if (turn) {
					color = "url('/static/orange1.jpg')";
					you++;
				} else {

					color = "url('/static/green1.jpg')";
					comp2++;
				}
				$("div.box[data-id='" + id + "']").css("background-image", color);
				boxes[id] = 4;
				//console.log(boxes.toString());

				$(".player2").text("You : " + you);
				$(".player1").text(comp2 + " : Comp");

				var full = true;
				for (var i = boxes.length - 1; i >= 0; i--) {
					if (boxes[i] != 4) {
						full = false;
						break;
					}
				}

				if (full){
					if (you>comp2) $("#turn").html("You are the winner <br/> Play again?");
				else if (you<comp2) $("#turn").html("Computer is the winner <br/> Play again?");
				else if(you == comp2)  $("#turn").html("It's a tie. Both won! <br/> Play again?");

				if (you>comp2) alert("You are the winner!");
				else if (you<comp2) alert("Computer is the winner!")
				else if(you == comp2)  alert("It's a tie!");
					}

					};
					break;
			case "pvc3": {
				if (turn) {
					color = "url('/static/orange3.jpg')";
					you++;
				} else {

					color = "url('/static/green3.jpg')";
					comp3++;
				}
				//i ostalo odozgo
				$("div.box[data-id='" + id + "']").css("background-image", color);
		boxes[id] = 4;
		//console.log(boxes.toString());

		$(".player2").text("You : " + you);
		$(".player1").text(comp3 + " : Comp");

		var full = true;
		for (var i = boxes.length - 1; i >= 0; i--) {
			if (boxes[i] != 4) {
				full = false;
				break;
			}
		}

		if(full){
			if (you>comp3) $("#turn").html("You are the winner <br/> Play again?");
			else if (you<comp3) $("#turn").html("Computer is the winner <br/> Play again?");
			else if(you == comp3)  $("#turn").html("It's a tie. Both won! <br/> Play again?");

			if (you>comp3) alert("You are the winner!");
			else if (you<comp3) alert("Computer is the winner!")
			else if(you == comp3)  alert("It's a tie!");
			}
		}
				break;
		}
	}



$(document).ready(function(){
    function getCookie(c_name) {
        if(document.cookie.length > 0) {
            c_start = document.cookie.indexOf(c_name + "=");
            if(c_start != -1) {
                c_start = c_start + c_name.length + 1;
                c_end = document.cookie.indexOf(";", c_start);
                if(c_end == -1) c_end = document.cookie.length;
                return unescape(document.cookie.substring(c_start,c_end));
            }
        }
        return "";
    }


    $(function () {
        $.ajaxSetup({
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            }
		});
		$.ajaxSetup({async: false});
    });
});
//minimax
function computer(mode) {
	//console.log(comp3);
	//console.log(you);
	$.post('/set_comp/', {comp: comp});
	$.post('/set_human/', {you: you});
	turn = false;
	var odabir;

	var proba = boxes.toString();
	console.log(proba);
	$.post('/validate_minimax/', {proba: proba}, function(data)
	{odabir=parseInt(data)});
	console.log(odabir);
	setTimeout(function(){computerSelect(odabir,mode);},500);
	//setTimeout(function(){console.log(odabir)},2700);
	//setTimeout(function(){computerSelect(odabir,mode)},2750);
	//setTimeout(function(){computerSelect(odabir,mode)},1000);

}
//minimax alfa-beta pruning sa jacom heuristikom
	function computer2(mode) {
		$.post('/set_comp2/', {comp2: comp2});
		$.post('/set_human/', {you: you});
		turn = false;
		var odabir =0;

		var proba = boxes.toString();
		console.log(proba);
		$.post('/validate_minimaxMedium/', {proba: proba}, function(data)
		{odabir=parseInt(data)});
		setTimeout(function(){computerSelect2(odabir,mode);},500);


	}
//tournament hard more..mozda samo najbolja heuristika?
	function computer3(mode) {
		//console.log(comp3);
		//console.log(you);
		$.post('/set_comp3/', {comp3: comp3});
		$.post('/set_human/', {you: you});
		turn = false;
		var odabir;
		var proba = boxes.toString();
		console.log(proba);
		$.post('/validate_minimaxHard/', {proba: proba}, function(data)
		{odabir=parseInt(data)});
		console.log(odabir);
		setTimeout(function(){computerSelect2(odabir,mode);},500);
		//setTimeout(function(){console.log(odabir)},2700);
		//setTimeout(function(){computerSelect(odabir,mode)},2750);
		//setTimeout(function(){computerSelect(odabir,mode)},1000);

	}
			//alert("Odgovor:" + data);}
		//var proba =JSON.stringify(boxes);
		/* $.ajax({
            type: "POST",
            url: '/validate_ajax/',
			data: proba

        })
        .done(function( data ) {
            alert( "Data: " + data );
		});
		*/





	function checkValid(t) {
		return ($(t).attr("data-active") === "false");
	}


	function Done(){
		done = true;
		for(i=0;i<boxes.length;i++)
		{
			if(boxes[i]!=4){
				done=false;
				break;}
		}
		return done;
	}



	function computerSelect(id,mode) {
		//ipak je kul

		$("div.line[data-line-1='" + id + "'], div.line[data-line-2='" + id + "']").each(function (i, v) {
			if (!$(v).hasClass("line-active"))
			/* &&(( boxes[parseInt($(v).attr("data-line-1"))]!=2 && boxes[parseInt($(v).attr("data-line-2"))]!=2 )
				|| (boxes[parseInt($(v).attr("data-line-1"))]==null || boxes[parseInt($(v).attr("data-line-2"))]==null )))
				*/
			 {
				var id1 = parseInt($(v).attr("data-line-1"));
				var id2 = parseInt($(v).attr("data-line-2"));



				if (checkValid(v) && turn === false) {

					if (id1 >= 0) var a = addValue(id1);
					if (id2 >= 0) var b = addValue(id2);
					$(v).addClass("line-active");
					$(v).attr("data-active", "true");

					if (Done()==true){
		        	$(".moves").append("<p>GAME OVER!</p>");
		        	return;}
		        	else {
					$(".moves").append("<p> " + $("#turn").text()+ " // Move: "+ id1 +", "+id2+ " .</p></br>");
					if (a === true || b === true) {
						switch(mode){
						case "pvc1":{
							$("#turn").text("Turn :" + "Comp-Easy");
							setTimeout(function(){computer(mode);},500);}
						break;
						case "pvc2":
							$("#turn").text("Turn :" + "Comp-Medium");
							setTimeout(function(){computer2(mode);},500);
						break;
						case "pvc3":
							$("#turn").text("Turn :" + "Comp-Hard");
							setTimeout(function(){computer3(mode);},500);

						break;
							}
					} else {
						turn = true;
						$("#turn").text("Turn :" + "You");
					}
				}
			}
			}

		});
	}

	function computerSelect2(id,mode) {
		//ipak je kul

		$("div.line[data-line-1='" + id + "'], div.line[data-line-2='" + id + "']").each(function (i, v) {
			if (!$(v).hasClass("line-active")
				&& boxes[parseInt($(v).attr("data-line-2"))]!=2
			)
			/* &&(( boxes[parseInt($(v).attr("data-line-1"))]!=2 && boxes[parseInt($(v).attr("data-line-2"))]!=2 )
				|| (boxes[parseInt($(v).attr("data-line-1"))]==null || boxes[parseInt($(v).attr("data-line-2"))]==null )))
				*/
			 {
				var id1 = parseInt($(v).attr("data-line-1"));
				var id2 = parseInt($(v).attr("data-line-2"));



				if (checkValid(v) && turn === false) {

					if (id1 >= 0) var a = addValue(id1);
					if (id2 >= 0) var b = addValue(id2);
					$(v).addClass("line-active");
					$(v).attr("data-active", "true");

					if (Done()==true){
		        	$(".moves").append("<p>GAME OVER!</p>");
		        	return;}
		        	else {
		        	   $(".moves").append("<p> " + $("#turn").text()+ " // Move: "+ id1 +", "+id2+ " .</p></br>");
					if (a === true || b === true) {
						switch(mode){
						case "pvc1":
							$("#turn").text("Turn :" + "Comp-Easy");
							setTimeout(function(){computer(mode);},500);
						break;
						case "pvc2":
							$("#turn").text("Turn :" + "Comp-Medium");
							setTimeout(function(){computer2(mode);},500);
						break;
						case "pvc3":
							$("#turn").text("Turn :" + "Comp-Hard");
							setTimeout(function(){computer3(mode);},500);

						break;
							}
					} else {
						turn = true;
						$("#turn").text("Turn :" + "You");
					}
				}
			}
			}


		});
		computerSelect(id,mode);
	}

	function random(min, max) {
		return Math.floor(Math.random() * (max - min + 1)) + min;
	}

	$(function () {
		$("#mode").click(function () {
			if($("#mode").val() == "pvc1" || $("#mode").val() == "pvc2" || $("#mode").val() == "pvc3" )
			$("#dubina").prop( "disabled", false );
		}
		);
		$("#pocni").click(function () {
			you1= 0
			you2 = 0
			comp = 0
			comp2 = 0
			comp3 = 0
			m = $("#redovi").val();
			n = $("#kolone").val();
			d = $("#dubina").val();
			mode = $("#mode").val();
			$.post('/set_dubina/', {d: d});

			load(m, n, mode);
		}
		);
	});


	/*
	function initialIdea() {
		turn = false;
		$("#turn").text("Turn : " + "Computer");

		setTimeout(function () {

			//play
			var length = boxes.length;

			var arr3 = [], arr2 = [], arr1 = [], arr0 = [];

			for (var i = length - 1; i >= 0; i--) {
				if (boxes[i] === 3) arr3.push(i);
				else if (boxes[i] === 2) arr2.push(i);
				else if (boxes[i] === 1) arr1.push(i);
				else arr0.push(i);
			}

			//best case
			if (arr3.length > 0) {
				computerSelect(arr3[random(0, arr3.length - 1)]);
			}

			//better case
			else if (arr1.length > 0) {
				computerSelect(arr1[random(0, arr1.length - 1)]);
			}

			//normal case
			else if (arr0.length > 0) {
				computerSelect(arr0[random(0, arr0.length - 1)]);
			}

			//worst case
			else if (arr2.length > 0) {
				computerSelect(arr2[random(0, arr2.length - 1)]);
			}

		}, 500);

	}
	*/
