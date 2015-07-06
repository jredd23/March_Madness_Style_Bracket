function update(game_id, win_game_id, win_game_val, home_team, selected) {
        var text = $('#' + selected).html();
	var val = $('#' + win_game_val).val();

	$('#' + game_id + '_val').attr("value", val);
	$('#' + game_id + '_hteam').removeClass("selected");
	$('#' + game_id + '_vteam').removeClass("selected");
	$('#' + selected).addClass("selected");
	if (win_game_id != "game67_champ") {
		if (home_team == 0) {
			$('#' + win_game_id + '_hteam').html(text);
	        	$('#' + win_game_id + '_hteam_val').attr("value", val);
		} else {
        	        $('#' + win_game_id + '_vteam').html(text);
                	$('#' + win_game_id + '_vteam_val').attr("value", val);
		}
	} else {
			$('#' + win_game_id ).html(text);
			checkFontSize();
	}

	checkForError(game_id);		

        var winner_game = $('#' + win_game_id + '_val').val();
        var winner_game_hteam = $('#' + win_game_id + '_hteam_val').val();
        var winner_game_vteam = $('#' + win_game_id + '_vteam_val').val();

	if (winner_game != winner_game_hteam && winner_game != winner_game_vteam) {
	        $('#' + win_game_id + '_val').attr("value", 0);
		if (home_team == 0) {
		        $('#' + win_game_id + '_hteam').removeClass("selected");
		} else {
		        $('#' + win_game_id + '_vteam').removeClass("selected");
		}
	}
}
function checkFontSize() {
	var html = $('#game67_champ').html();
	if (html.length > 14) {
        	$('#game67_champ').css("font-size", "smaller");
	} else {
                $('#game67_champ').css("font-size", "medium");
	}
}

function validateForm() {
	var return_val = true;
	for (i = 1; i < 68; i++) {
		var test = "game" + i;
		var test_val = document.forms['create'][test].value;
		if ( test_val < 1) {
			$("#" + test).addClass("error");
			$("#" + test + "_label").show();
			return_val = false;
		} else {
			$("#" + test).removeClass("error");
			$("#" + test + "_label").hide();
		}
	}
	
	return return_val;
}
function checkForError(gameId) {
	var test = gameId;
        var test_val = document.forms['create'][test].value;
	if ( test_val > 0) {
		$("#" + test).removeClass("error");
                $("#" + test + "_label").hide();
	}
}

function champ_game(game_id, win_game_id) {
        var winner_game = document.getElementById(win_game_id);
        var game = document.getElementById(game_id);
	var text = game.options[game.selectedIndex].text;
        var val = game.options[game.selectedIndex].value;
	var champ_id = win_game_id;

	champ_id += '_val';

	var champ_val = document.getElementById(champ_id);
	winner_game.value=text;
	champ_val.value=val;
	
}

function champ(game_id, win_game_id, win_game_val) {
        var winner_game = document.getElementById(win_game_id);
        var game = document.getElementById(game_id);
	var val_in = document.getElementById(win_game_val);
        var text = game.value;
	var champ = document.getElementById('game67');
	var val = val_in.value;
        winner_game.value=text;
	champ.value = val;

	var select = document.getElementById(win_game_id);
	var option = document.createElement("option");

	option.text = text;
	option.value = val;
	option.id = "hteam";
	select.remove(0);
	select.add(option,select[0]);
	select.selectedIndex = "0";

}

function tiebreak(range, val) {
	var input = document.getElementById(range);
	var update = document.getElementById(val);
	var value = input.value;
	update.value = value;
}

function setNav(cur_nav) {
	$('#nav_' + cur_nav).addClass("active");
}

function firstFour(game_id, team, region_id) {
	seed = $('#' + game_id + '_' + team + '_seed').val();
	if (region_id == 1) {
		if (seed == 1 || seed == 16) {
			update_game = 5;
		} else if ( seed == 8 || seed == 9) {
			update_game = 6;
                } else if ( seed == 5 || seed == 12) {
                        update_game = 7;
                } else if ( seed == 4 || seed == 13) {
                        update_game = 8;
                } else if ( seed == 6 || seed == 11) {
                        update_game = 9;
                } else if ( seed == 3|| seed == 14) {
                        update_game = 10;
                } else if ( seed == 7 || seed == 10) {
                        update_game = 11;
                } else if ( seed == 2 || seed == 15) {
                        update_game = 12;
		}
                $('#r64_r1_ff_game').val(update_game);
		if ( seed < 9) {
			$('#r64_r1_ff_team').val('hteam');
		} else {
			$('#rg_r1_ff_team').val('vteam');
		}
		for ( i = 5; i < 13; i++) {
			if ($('#game_' + i + '_hteam_name').val() == 'Winner of First Four Game') {
				$('#game_' + i + '_hteam_name').val('');
			}
			if ($('#game_' + i + '_vteam_name').val() == 'Winner of First Four Game') {
				$('#game_' + i + '_vteam_name').val('');
                        }
 
	                $('#game_' + i + '_hteam_name').prop('required', true);
        	        $('#game_' + i + '_hteam_name').prop('disabled', false);
	                $('#game_' + i + '_vteam_name').prop('required', true);
	                $('#game_' + i + '_vteam_name').prop('disabled', false);
		}
	} else if (region_id == 2) {
                if (seed == 1 || seed == 16) {
                        update_game = 21;
                } else if ( seed == 8 || seed == 9) {
                        update_game = 22;
                } else if ( seed == 5 || seed == 12) {
                        update_game = 23;
                } else if ( seed == 4 || seed == 13) {
                        update_game = 24;
                } else if ( seed == 6 || seed == 11) {
                        update_game = 25;
                } else if ( seed == 3|| seed == 14) {
                        update_game = 26;
                } else if ( seed == 7 || seed == 10) {
                        update_game = 27;
                } else if ( seed == 2 || seed == 15) {
                        update_game = 28;
                }
                $('#r64_r2_ff_game').val(update_game);
                if ( seed < 9) {
                        $('#r64_r2_ff_team').val('hteam');
                } else {
                        $('#rg_r2_ff_team').val('vteam');
                }
                for ( i = 21; i < 29; i++) {
                        if ($('#game_' + i + '_hteam_name').val() == 'Winner of First Four Game') {
                                $('#game_' + i + '_hteam_name').val('');
                        }
                        if ($('#game_' + i + '_vteam_name').val() == 'Winner of First Four Game') {
                                $('#game_' + i + '_vteam_name').val('');
                        }

                        $('#game_' + i + '_hteam_name').prop('required', true);
                        $('#game_' + i + '_hteam_name').prop('disabled', false);
                        $('#game_' + i + '_vteam_name').prop('required', true);
                        $('#game_' + i + '_vteam_name').prop('disabled', false);
                }
        } else if (region_id == 3) {
                if (seed == 1 || seed == 16) {
                        update_game = 13;
                } else if ( seed == 8 || seed == 9) {
                        update_game = 14;
                } else if ( seed == 5 || seed == 12) {
                        update_game = 15;
                } else if ( seed == 4 || seed == 13) {
                        update_game = 16;
                } else if ( seed == 6 || seed == 11) {
                        update_game = 17;
                } else if ( seed == 3|| seed == 14) {
                        update_game = 18;
                } else if ( seed == 7 || seed == 10) {
                        update_game = 19;
                } else if ( seed == 2 || seed == 15) {
                        update_game = 20;
                }
                $('#r64_r3_ff_game').val(update_game);
                if ( seed < 9) {
                        $('#r64_r3_ff_team').val('hteam');
                } else {
                        $('#rg_r3_ff_team').val('vteam');
                }
                for ( i = 13; i < 21; i++) {
                        if ($('#game_' + i + '_hteam_name').val() == 'Winner of First Four Game') {
                                $('#game_' + i + '_hteam_name').val('');
                        }
                        if ($('#game_' + i + '_vteam_name').val() == 'Winner of First Four Game') {
                                $('#game_' + i + '_vteam_name').val('');
                        }

                        $('#game_' + i + '_hteam_name').prop('required', true);
                        $('#game_' + i + '_hteam_name').prop('disabled', false);
                        $('#game_' + i + '_vteam_name').prop('required', true);
                        $('#game_' + i + '_vteam_name').prop('disabled', false);
                }
        } else if (region_id == 4) {
                if (seed == 1 || seed == 16) {
                        update_game = 29;
                } else if ( seed == 8 || seed == 9) {
                        update_game = 30;
                } else if ( seed == 5 || seed == 12) {
                        update_game = 31;
                } else if ( seed == 4 || seed == 13) {
                        update_game = 32;
                } else if ( seed == 6 || seed == 11) {
                        update_game = 33;
                } else if ( seed == 3|| seed == 14) {
                        update_game = 34;
                } else if ( seed == 7 || seed == 10) {
                        update_game = 35;
                } else if ( seed == 2 || seed == 15) {
                        update_game = 36;
                }
                $('#r64_r4_ff_game').val(update_game);
                if ( seed < 9) {
                        $('#r64_r4_ff_team').val('hteam');
                } else {
                        $('#rg_r4_ff_team').val('vteam');
                }
                for ( i = 29; i < 37; i++) {
                        if ($('#game_' + i + '_hteam_name').val() == 'Winner of First Four Game') {
                                $('#game_' + i + '_hteam_name').val('');
                        }
                        if ($('#game_' + i + '_vteam_name').val() == 'Winner of First Four Game') {
                                $('#game_' + i + '_vteam_name').val('');
                        }

                        $('#game_' + i + '_hteam_name').prop('required', true);
                        $('#game_' + i + '_hteam_name').prop('disabled', false);
                        $('#game_' + i + '_vteam_name').prop('required', true);
                        $('#game_' + i + '_vteam_name').prop('disabled', false);
                }
	}
        if (team == 'hteam') {
                $('#' + game_id + '_vteam_seed').val(seed);
        } else {
                $('#' + game_id + '_hteam_seed').val(seed);
        }
	if ( seed < 9) {
                $('#game_' + update_game + '_hteam_name').val('Winner of First Four Game');
                $('#game_' + update_game + '_hteam_name').removeAttr('required');
                $('#game_' + update_game + '_hteam_name').prop('disabled', true);
	} else {
                $('#game_' + update_game + '_vteam_name').val('Winner of First Four Game');
                $('#game_' + update_game + '_vteam_name').removeAttr('required');
                $('#game_' + update_game + '_vteam_name').prop('disabled', true);
	}
	$('#' + game_id + '_win_game').attr('value',update_game);

}

function clearContent() {
	cur_content = $('#new_content').html();
        if ( cur_content == "Rule Specifics") {
		$('#new_content').html('');	
	}
}
function AsyncConfirmYesNo(title, msg, yesFn, noFn) {
    var $confirm = $("#modalConfirmYesNo");
    $confirm.modal('show');
    $("#lblTitleConfirmYesNo").html(title);
    $("#lblMsgConfirmYesNo").html(msg);
    $("#btnYesConfirmYesNo").off('click').click(function () {
        yesFn();
        $confirm.modal("hide");
    });
    $("#btnNoConfirmYesNo").off('click').click(function () {
        noFn();
        $confirm.modal("hide");
    });
}
function ShowConfirmYesNo() {
    AsyncConfirmYesNo(
        "Confirm Deletion",
        "Are you sure you want to delete this rule?",
        MyYesFunction,
        MyNoFunction
    );
}
function MyYesFunction() {
    $('#rules_del_form').submit();
}
function MyNoFunction() {
}


