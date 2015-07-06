$(document).ready(function() {
    firstFour('game_1', 'hteam', 1);
    firstFour('game_2', 'hteam', 2);
    firstFour('game_3', 'hteam', 3);
    firstFour('game_4', 'hteam', 4);
    var site_form = $('#site_form');
    
    site_form.on('submit', function(e) {
        e.preventDefault();
        $.ajax({
            url : "/update_site/",
            type : "POST",
            data : site_form.serialize(),
            beforeSend: function() {
            },
            success: function(json) {
                $('#site_name').attr('value',json.site_name);
                $('#sweet_16').attr('value',json.sweet_16);
                $('#region_1').attr('value',json.region_1);
                $('#region_2').attr('value',json.region_2);
                $('#region_3').attr('value',json.region_3);
                $('#region_4').attr('value',json.region_4);
                $('#region_1_team_title').html(json.region_1);
                $('#region_2_team_title').html(json.region_2);
                $('#region_3_team_title').html(json.region_3);
                $('#region_4_team_title').html(json.region_4);
                $('#region_1_dropdown').html(json.region_1);
                $('#region_2_dropdown').html(json.region_2);
                $('#region_3_dropdown').html(json.region_3);
                $('#region_4_dropdown').html(json.region_4);
                $('#title_site_name').html(json.site_name);
		$('#r1_body').html('Congratulations!<br>All ' + json.region_1 + ' teams have been updated.');
                $('#r2_body').html('Congratulations!<br>All ' + json.region_2 + ' teams have been updated.');
                $('#r3_body').html('Congratulations!<br>All ' + json.region_3 + ' teams have been updated.');
                $('#r4_body').html('Congratulations!<br>All ' + json.region_4 + ' teams have been updated.');

		$('#site_modal').modal('show');
            },
            error : function(xhr,errmsg,err) {
                alert("error");
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                $('#results').append(xhr.responseText);
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    });

    var first_four = $('#first_four_form');

    first_four.on('submit', function(e) {
	e.preventDefault();
        $.ajax({
            url : "/update_ff/",
            type : "POST",
            data : first_four.serialize(),
            beforeSend: function() {
            },
            success: function(json) {
                $('#ff_modal').modal('show');
            },
            error : function(xhr,errmsg,err) {
                alert("error");
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                $('#results').append(xhr.responseText);
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    });

    var region_1 = $('#r64_region_1_form');

    region_1.on('submit', function(e) {
        e.preventDefault();
        $.ajax({
            url : "/update_r64_r1/",
            type : "POST",
            data : region_1.serialize(),
            beforeSend: function() {
            },
            success: function(json) {
                $('#r64_r1_modal').modal('show');
            },
            error : function(xhr,errmsg,err) {
                alert("error");
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                $('#results').append(xhr.responseText);
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    });

    var region_2 = $('#r64_region_2_form');

    region_2.on('submit', function(e) {
        e.preventDefault();
        $.ajax({
            url : "/update_r64_r2/",
            type : "POST",
            data : region_2.serialize(),
            beforeSend: function() {
            },
            success: function(json) {
                $('#r64_r2_modal').modal('show');
            },
            error : function(xhr,errmsg,err) {
                alert("error");
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                $('#results').append(xhr.responseText);
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    });
    var region_3 = $('#r64_region_3_form');

    region_3.on('submit', function(e) {
        e.preventDefault();
        $.ajax({
            url : "/update_r64_r3/",
            type : "POST",
            data : region_3.serialize(),
            beforeSend: function() {
            },
            success: function(json) {
                $('#r64_r3_modal').modal('show');
            },
            error : function(xhr,errmsg,err) {
                alert("error");
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                $('#results').append(xhr.responseText);
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    });

    var region_4 = $('#r64_region_4_form');

    region_4.on('submit', function(e) {
        e.preventDefault();
        $.ajax({
            url : "/update_r64_r4/",
            type : "POST",
            data : region_4.serialize(),
            beforeSend: function() {
            },
            success: function(json) {
                $('#r64_r4_modal').modal('show');
            },
            error : function(xhr,errmsg,err) {
                alert("error");
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                $('#results').append(xhr.responseText);
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    });

    var rules_edit = $('#rules_edit_form');

    rules_edit.on('submit', function(e) {
        e.preventDefault();
        $.ajax({
            url : "/update_rules_edit/",
            type : "POST",
            data : rules_edit.serialize() + "&edit_content=" + $('#edit_content').html(),
            beforeSend: function() {
            },
            success: function(json) {
                $('#rules_edit_modal').modal('show');
            },
            error : function(xhr,errmsg,err) {
                alert("error");
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                $('#results').append(xhr.responseText);
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    });

    var rules_new = $('#rules_new_form');

    rules_new.on('submit', function(e) {
        e.preventDefault();
        $.ajax({
            url : "/update_rules_new/",
            type : "POST",
            data : rules_new.serialize() + "&new_content=" + $('#new_content').html(),
            beforeSend: function() {
            },
            success: function(json) {
		$('#edit_title').append('<option value="' + json.new_id + '">' + json.new_title + '</option>');
                $('#del_title').append('<option value="' + json.new_id + '">' + json.new_title + '</option>');
		$('#new_title_name').val("");
		$('#new_content').html("Rule Specifics");
                $('#rules_new_modal').modal('show');
            },
            error : function(xhr,errmsg,err) {
                alert("error");
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                $('#results').append(xhr.responseText);
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    });

    var rules_edit_select = $('#edit_title');
    
    rules_edit_select.on('change', function(e) {
        e.preventDefault();
        $.ajax({
            url : "/update_rules_edit_change/",
            type : "POST",
            data : rules_edit.serialize(),
            beforeSend: function() {
            },
            success: function(json) {
		$('#edit_title_name').attr("value",json.rule_title);
                $('#edit_content').html(json.rule_content);
            },
            error : function(xhr,errmsg,err) {
                alert("error");
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                $('#results').append(xhr.responseText);
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    });

    var rules_del = $('#rules_del_form');

    rules_del.on('submit', function(e) {
        e.preventDefault();
        $.ajax({
            url : "/update_rules_del/",
            type : "POST",
            data : rules_del.serialize(),
            success: function(json) {
		$('#del_title option:selected').remove();
		$('#del_title').val('1');
		$('#del_title_name').attr("value", json.rule_title);
		$('#del_content').html(json.rule_content);
		$('#edit_title option[value=' + json.rule_id + ']').remove();
                $('#rules_del_modal').modal('show');
            },
            error : function(xhr,errmsg,err) {
                alert("error");
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                $('#results').append(xhr.responseText);
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    });

    var rules_del_select = $('#del_title');

    rules_del_select.on('change', function(e) {
        e.preventDefault();
        $.ajax({
            url : "/update_rules_del_change/",
            type : "POST",
            data : rules_del.serialize(),
            beforeSend: function() {
            },
            success: function(json) {
                $('#del_title_name').attr("value",json.rule_title);
                $('#del_content').html(json.rule_content);
            },
            error : function(xhr,errmsg,err) {
                alert("error");
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                $('#results').append(xhr.responseText);
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    });

});

