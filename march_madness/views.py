from io import BytesIO
import os.path
import datetime
import pytz


from django.conf import settings
from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage
from django.db import connection
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from  reportlab.lib.units import cm, inch

from march_madness.models import Games, Rounds, Regions, Teams, Blog, Brackets, ScoringValues, SmackTalk, Rules, Site
from march_madness.forms import POSTForm

def getCords(start_x , end_x):
    if start_x > end_x:
        x = (start_x - end_x) / 2
    else:
        x = (end_x - start_x) / 2
    return x

def getFirstFour(game_list, team_list):
    first_four = []

    for game in game_list.values():
        if game['game_round_id'] == 1:
            hteam = ""
            vteam = ""
            hteam_seed = 0
            vteam_seed = 0
            for team in team_list.values():
                if team['id'] == game['hteam']:
                    hteam = team['team_name']
                    hteam_seed = """({})""".format(team['team_seed'])
                if team['id'] == game['vteam']:
                    vteam = team['team_name']
                    vteam_seed = """({})""".format(team['team_seed'])
                if game['vteam'] == 0:
                    vteam = ""
                    vteam_seed = ""
                if game['hteam'] == 0:
                    hteam = ""
                    hteam_seed = ""

            first_four.append([game['id'], game['win_game_id'], game['win_home'], game['hteam'], hteam, game['vteam'], vteam, hteam_seed, vteam_seed])
    return first_four

def getRoundGames(game_list, team_list, round_id, region_id):
    games = []
    for game in game_list.values():
        if game['game_round_id'] == round_id:
            if game['game_region_id'] == region_id:
                hteam = ""
                vteam = ""
                hteam_seed = 0
                vteam_seed = 0
                for team in team_list.values():
                    if team['id'] == game['hteam']:
                        hteam = team['team_name']
                        hteam_seed = """({})""".format(team['team_seed'])
                    if team['id'] == game['vteam']:
                        vteam = team['team_name']
                        vteam_seed = """({})""".format(team['team_seed'])
                    if game['vteam'] == 0:
                        vteam = ""
                        vteam_seed = ""
                    if game['hteam'] == 0:
                        hteam = ""
                        hteam_seed = ""

                games.append([game['id'], game['win_game_id'], game['win_home'], game['hteam'], hteam, game['vteam'], vteam, hteam_seed, vteam_seed])
    return games

def get_bracket(bracket_id, games, teams):
    game_set = []
    first_four = []
    round_1_region_1 = []
    round_1_region_2 = []
    round_1_region_3 = []
    round_1_region_4 = []
    round_2_region_1 = []
    round_2_region_2 = []
    round_2_region_3 = []
    round_2_region_4 = []
    round_3_region_1 = []
    round_3_region_2 = []
    round_3_region_3 = []
    round_3_region_4 = []
    round_4_region_1 = []
    round_4_region_2 = []
    round_4_region_3 = []
    round_4_region_4 = []
    round_5_region_1 = []
    round_5_region_2 = []
    round_6_region_1 = []
    round_7_region_1 = []

    bracket = Brackets.objects.filter(id= bracket_id).values()
    for x in games.values():
        if x['id'] < 37 and x['vteam'] != 0:
            game_set.append([x['id'], x['win_game_id'], x['win_home'], x['hteam'], x['vteam'], x['game_round_id'], x['game_region_id']])
        elif x['id'] < 37:
            game_id = "game{}".format(x['vteam_from'])
            game_set.append([x['id'], x['win_game_id'], x['win_home'], x['hteam'], bracket[0][game_id], x['game_round_id'], x['game_region_id']])
        else:
            home_game_id = "game{}".format(x['hteam_from'])
            vis_game_id = "game{}".format(x['vteam_from'])
            game_set.append([x['id'], x['win_game_id'], x['win_home'], bracket[0][home_game_id], bracket[0][vis_game_id], x['game_round_id'], x['game_region_id']])
    for x in game_set:
        z = int(x[0] - 1)
        a = x[0]
        for y in teams.values():
            if x[3] == y['id']:
                hteam = y['team_name']
                hteam_seed = "({})".format(y['team_seed'])
            if x[4] == y['id']:
                vteam = y['team_name']
                vteam_seed = "({})".format(y['team_seed'])
        game_id = "game{}".format(a)
        if bracket[0][game_id] == x[3]:
            selected = "hteam"
        else:
            selected = "vteam"
        if x[5] == 1:
            first_four.append([x[0], x[1], x[2], x[3], hteam, x[4], vteam, hteam_seed, vteam_seed, selected])
        elif x[5] == 2 and x[6] == 1:
            round_1_region_1.append([x[0], x[1], x[2], x[3], hteam, x[4], vteam, hteam_seed, vteam_seed, selected])
        elif x[5] == 2 and x[6] == 2:
            round_1_region_2.append([x[0], x[1], x[2], x[3], hteam, x[4], vteam, hteam_seed, vteam_seed, selected])
        elif x[5] == 2 and x[6] == 3:
            round_1_region_3.append([x[0], x[1], x[2], x[3], hteam, x[4], vteam, hteam_seed, vteam_seed, selected])
        elif x[5] == 2 and x[6] == 4:
            round_1_region_4.append([x[0], x[1], x[2], x[3], hteam, x[4], vteam, hteam_seed, vteam_seed, selected])
        elif x[5] == 3 and x[6] == 1:
            round_2_region_1.append([x[0], x[1], x[2], x[3], hteam, x[4], vteam, hteam_seed, vteam_seed, selected])
        elif x[5] == 3 and x[6] == 2:
            round_2_region_2.append([x[0], x[1], x[2], x[3], hteam, x[4], vteam, hteam_seed, vteam_seed, selected])
        elif x[5] == 3 and x[6] == 3:
            round_2_region_3.append([x[0], x[1], x[2], x[3], hteam, x[4], vteam, hteam_seed, vteam_seed, selected])
        elif x[5] == 3 and x[6] == 4:
            round_2_region_4.append([x[0], x[1], x[2], x[3], hteam, x[4], vteam, hteam_seed, vteam_seed, selected])
        elif x[5] == 4 and x[6] == 1:
            round_3_region_1.append([x[0], x[1], x[2], x[3], hteam, x[4], vteam, hteam_seed, vteam_seed, selected])
        elif x[5] == 4 and x[6] == 2:
            round_3_region_2.append([x[0], x[1], x[2], x[3], hteam, x[4], vteam, hteam_seed, vteam_seed, selected])
        elif x[5] == 4 and x[6] == 3:
            round_3_region_3.append([x[0], x[1], x[2], x[3], hteam, x[4], vteam, hteam_seed, vteam_seed, selected])
        elif x[5] == 4 and x[6] == 4:
            round_3_region_4.append([x[0], x[1], x[2], x[3], hteam, x[4], vteam, hteam_seed, vteam_seed, selected])
        elif x[5] == 5 and x[6] == 1:
            round_4_region_1.append([x[0], x[1], x[2], x[3], hteam, x[4], vteam, hteam_seed, vteam_seed, selected])
        elif x[5] == 5 and x[6] == 2:
            round_4_region_2.append([x[0], x[1], x[2], x[3], hteam, x[4], vteam, hteam_seed, vteam_seed, selected])
        elif x[5] == 5 and x[6] == 3:
            round_4_region_3.append([x[0], x[1], x[2], x[3], hteam, x[4], vteam, hteam_seed, vteam_seed, selected])
        elif x[5] == 5 and x[6] == 4:
            round_4_region_4.append([x[0], x[1], x[2], x[3], hteam, x[4], vteam, hteam_seed, vteam_seed, selected])
        elif x[5] == 6 and x[6] == 1:
            round_5_region_1.append([x[0], x[1], x[2], x[3], hteam, x[4], vteam, hteam_seed, vteam_seed, selected])
        elif x[5] == 6 and x[6] == 2:
            round_5_region_2.append([x[0], x[1], x[2], x[3], hteam, x[4], vteam, hteam_seed, vteam_seed, selected])
        elif x[5] == 7 and x[6] == 1:
            round_6_region_1.append([x[0], x[1], x[2], x[3], hteam, x[4], vteam, hteam_seed, vteam_seed, selected])
            if selected == 'hteam':
                round_7_region_1.append([x[0], x[1], x[2], x[3], hteam, x[3], hteam, hteam_seed, hteam_seed, selected])
            else:
                round_7_region_1.append([x[0], x[1], x[2], x[4], vteam, x[4], vteam, vteam_seed, vteam_seed, selected])
    return first_four, round_1_region_1, round_1_region_2, round_1_region_3, round_1_region_4, round_2_region_1, round_2_region_2, round_2_region_3, round_2_region_4, round_3_region_1, round_3_region_2, round_3_region_3, round_3_region_4, round_4_region_1, round_4_region_2, round_4_region_3, round_4_region_4, round_5_region_1, round_5_region_2, round_6_region_1, round_7_region_1

def emailPdf(user_name, email_address, file_name ):
    subject = 'Thank you for your Submission: %s' % user_name
    body = '%s: \n  Thank you for submitting your Bracket! \n Your local Commissioner' % user_name
    msg = EmailMessage( subject, body, 'submisstion@unifiedgroup.com', [email_address] )
    msg.attach_file(file_name)
    msg.send()
    return msg

def getPdf(bracket_id, username):
    rounds_h = [
        (31, 20, 85, 550, 535,15, "Round of 64"),
        (15, 85, 150, 542, 512,30, "Round of 32"),
        (7, 150, 215, 527, 467, 60, "Sweet 16"),
        (3, 215, 280, 497, 377, 120, "Elite 8"),
        (1, 280, 345, 437, 197, 240, "Final Four"),
        (31, 780,715, 550,535,15, "Round of 64"),
        (15, 715, 650, 542, 512,30, "Round of 32"),
        (7, 650, 585, 527, 467, 60, "Elite 8"),
        (3, 585, 520, 497, 377, 120, "Sweet 16"),
        (1, 520, 455, 437, 197, 240, "Final Four"),
    ]
    first_four_champ = [
        (345, 377, 410, 377),
        (455, 257, 390, 257),
        (360, 337, 440, 337),
        (360, 297, 440, 297),
        (360, 337, 360, 297),
        (440, 337, 440, 297),
        (250, 535, 315, 535),
        (250, 565, 250, 535),
        (315, 565, 315, 535),
        (325, 535, 390, 535),
        (325, 565, 325, 535),
        (390, 565, 390, 535),
        (400, 535, 465, 535),
        (400, 565, 400, 535),
        (465, 565, 465, 535),
        (475, 535, 540, 535),
        (475, 565, 475, 535),
        (540, 565, 540, 535),
        (250, 535, 250, 515),
        (250, 515, 540, 515),
        (540, 535, 540, 515),
        (250, 565, 540, 565),
        (360, 187, 440, 187),
        (360, 147, 440, 147),
        (360, 187, 360, 147),
        (440, 187, 440, 147),

    ]

    bracket = []
    for x in rounds_h:
        for y in range(x[0]):
            step = y * x[5]
            line = (x[1], x[3] - step, x[2], x[3] - step)
            line2 = (x[1], x[4] - step, x[2], x[4] - step)
            if y % 2 == 0:
                line3 = (x[2], x[3] - step, x[2], x[4] - step)
                bracket.append(line3)
            bracket.append(line)
            bracket.append(line2)

    bracket_set = Brackets.objects.filter(id = bracket_id)
    team = Teams.objects.all()
    games = Games.objects.all()
    game_set = {}
    team_text_len = 24
    tie_breaker = ""
    bracket_name = ""
    for x in range(68):
        game_set[x] = {}

    for x in range(1,68):
        game_id = "game"
        a = str(x)
        b = x - 1
        game_id = game_id + a
        for y in bracket_set.values():
            tie_breaker = str(y['tiebreaker'])
            bracket_name = str(y['name'])
            for c in games.values():
                if c['id'] == x:
                    if c['id'] < 37:
                        for z in team:
                            if c['hteam'] == z.id:
                                team_text = "({}) {}".format(z.team_seed, z.team_name)
                                if len(team_text) > team_text_len:
                                    team_text = team_text[:team_text_len]

                                win_game_id = c['win_game_id'] - 1
                                game_win = "Game Winner"
                                game_set[b].update({game_win : team_text})
                                if c['win_home'] == 0:
                                    game_set[win_game_id].update({"Home Team" : team_text})
                                else:
                                    game_set[win_game_id].update({"Away Team" : team_text})
                                game_set[b].update({"Home Team" : team_text})
                            if c['vteam'] == z.id:
                                team_text = "({}) {}".format(z.team_seed, z.team_name)
                                if len(team_text) > team_text_len:
                                    team_text = team_text[:team_text_len]

                                win_game_id = c['win_game_id'] - 1
                                game_win = "Game Winner"
                                game_set[b].update({game_win : team_text})
                                if c['win_home'] == 0:
                                    game_set[win_game_id].update({"Home Team" : team_text})
                                else:
                                    game_set[win_game_id].update({"Away Team" : team_text})
                                game_set[b].update({"Away Team" : team_text})
                    else:
                        for z in team:
                            if y[game_id] == z.id:
                                team_text = "({}) {}".format(z.team_seed, z.team_name)
                                if len(team_text) > team_text_len:
                                    team_text = team_text[:team_text_len]

                                win_game_id = c['win_game_id'] - 1
                                game_win = "Game Winner"
                                game_set[b].update({game_win : team_text})
                                if c['win_home'] == 0:
                                    game_set[win_game_id].update({"Home Team" : team_text})
                                else:
                                    game_set[win_game_id].update({"Away Team" : team_text})
    bracket_id_str = str(bracket_id)
    save_name = bracket_id_str + "_" + username + "_" + bracket_name + ".pdf"
    full_name =  os.path.join(settings.MEDIA_ROOT, save_name)
    file_name = "'attachment; filename=" + full_name
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = file_name

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas( full_name, pagesize=landscape(letter))

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.setFont('Helvetica', 10)
    p.drawCentredString( 52 , 580, rounds_h[0][6])
    p.drawCentredString( 117 , 580, rounds_h[1][6])
    p.drawCentredString( 182 , 580, rounds_h[2][6])
    p.drawCentredString( 247 , 580, rounds_h[3][6])
    p.drawCentredString( 312 , 580, rounds_h[4][6])
    p.drawCentredString( 748 , 580, rounds_h[5][6])
    p.drawCentredString( 683 , 580, rounds_h[6][6])
    p.drawCentredString( 618 , 580, rounds_h[7][6])
    p.drawCentredString( 553 , 580, rounds_h[8][6])
    p.drawCentredString( 488 , 580, rounds_h[9][6])
    p.drawCentredString( 52 , 50, rounds_h[0][6])
    p.drawCentredString( 117 , 50, rounds_h[1][6])
    p.drawCentredString( 182 , 50, rounds_h[2][6])
    p.drawCentredString( 247 , 50, rounds_h[3][6])
    p.drawCentredString( 312 , 50, rounds_h[4][6])
    p.drawCentredString( 748 , 50, rounds_h[5][6])
    p.drawCentredString( 683 , 50, rounds_h[6][6])
    p.drawCentredString( 618 , 50, rounds_h[7][6])
    p.drawCentredString( 553 , 50, rounds_h[8][6])
    p.drawCentredString( 488 , 50, rounds_h[9][6])
    p.drawCentredString( 400 , 50, "National Championship")
    p.drawCentredString( 400 , 580, "National Championship")
    p.drawCentredString( 400 , 520, "First Four")
    p.drawCentredString( 400 , 137, "Tie Breaker")

    p.lines(bracket)
    p.lines(first_four_champ)

    p.setFont('Helvetica', 6)
    for x in range(68):
        x_cord_64_a = 54
        x_cord_64_b = 749
        x_cord_four = 284
        y_cord_home = 555
        y_cord_away = 540
        if x < 4:
            step = x * 75
            p.drawCentredString( x_cord_four + step, y_cord_home, game_set[x]['Home Team'])
            p.drawCentredString( x_cord_four + step, y_cord_away, game_set[x]['Away Team'])
        if x > 3 and x < 20 :
            step = (x - 4) * 30
            p.drawCentredString( x_cord_64_a, y_cord_home - step, game_set[x]['Home Team'])
            p.drawCentredString( x_cord_64_a, y_cord_away - step, game_set[x]['Away Team'])
        if x > 19 and x < 36 :
            step = (x - 20) * 30
            p.drawCentredString( x_cord_64_b, y_cord_home - step, game_set[x]['Home Team'])
            p.drawCentredString( x_cord_64_b, y_cord_away - step, game_set[x]['Away Team'])
        if x > 35 and x < 44:
            stepx = 65 + x_cord_64_a
            stepy_a = ((x - 36) * 60) + 8
            stepy_b = ((x - 36) * 60) + 26
            p.drawCentredString( stepx , y_cord_home - stepy_a, game_set[x]['Home Team'])
            p.drawCentredString( stepx , y_cord_away - stepy_b, game_set[x]['Away Team'])
        if x > 43 and x < 52:
            stepx = x_cord_64_b - 65
            stepy_a = ((x - 44) * 60) + 8
            stepy_b = ((x - 44) * 60) + 26
            p.drawCentredString( stepx , y_cord_home - stepy_a, game_set[x]['Home Team'])
            p.drawCentredString( stepx , y_cord_away - stepy_b, game_set[x]['Away Team'])
        if x > 51 and x < 56:
            stepx = x_cord_64_a + 130
            stepy_a = ((x - 52) * 120) + 25
            stepy_b = ((x - 52) * 120) + 70
            p.drawCentredString( stepx , y_cord_home - stepy_a, game_set[x]['Home Team'])
            p.drawCentredString( stepx , y_cord_away - stepy_b, game_set[x]['Away Team'])
        if x > 55 and x < 60:
            stepx = x_cord_64_b - 130
            stepy_a = ((x - 56) * 120) + 25
            stepy_b = ((x - 56) * 120) + 70
            p.drawCentredString( stepx , y_cord_home - stepy_a, game_set[x]['Home Team'])
            p.drawCentredString( stepx , y_cord_away - stepy_b, game_set[x]['Away Team'])
        if x > 59 and x < 62:
            stepx = x_cord_64_a + 195
            stepy_a = ((x - 60) * 240) + 55
            stepy_b = ((x - 60) * 240) + 160
            p.drawCentredString( stepx , y_cord_home - stepy_a, game_set[x]['Home Team'])
            p.drawCentredString( stepx , y_cord_away - stepy_b, game_set[x]['Away Team'])
        if x > 61 and x < 64:
            stepx = x_cord_64_b - 195
            stepy_a = ((x - 62) * 240) + 55
            stepy_b = ((x - 62) * 240) + 160
            p.drawCentredString( stepx , y_cord_home - stepy_a, game_set[x]['Home Team'])
            p.drawCentredString( stepx , y_cord_away - stepy_b, game_set[x]['Away Team'])
        if x == 64 :
            stepx = x_cord_64_a + 260
            stepy_a = ((x - 64) * 240) + 115
            stepy_b = ((x - 64) * 240) + 340
            p.drawCentredString( stepx , y_cord_home - stepy_a, game_set[x]['Home Team'])
            p.drawCentredString( stepx , y_cord_away - stepy_b, game_set[x]['Away Team'])
            p.drawCentredString( x_cord_64_a + 325, y_cord_home - 175, game_set[x]['Game Winner'])
        if x == 65:
            stepx = x_cord_64_b - 260
            stepy_a = ((x - 65) * 240) + 115
            stepy_b = ((x - 65) * 240) + 340
            p.drawCentredString( stepx , y_cord_home - stepy_a, game_set[x]['Home Team'])
            p.drawCentredString( stepx , y_cord_away - stepy_b, game_set[x]['Away Team'])
            p.drawCentredString( x_cord_64_b - 325, y_cord_away - 280, game_set[x]['Game Winner'])
        if x == 66:
            p.setFont('Helvetica', 8)
            p.drawCentredString( 400, 315, game_set[x]['Game Winner'])

    p.setFont('Helvetica', 12)
    p.drawCentredString( 400, 340, "National")
    p.drawCentredString( 400, 285, "Champion")
    p.setFont('Helvetica', 16)
    p.drawCentredString( 400, 165, tie_breaker)
    p.drawCentredString( 400, 100, bracket_name)

    # Close the PDF object cleanly.
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return save_name, full_name

def path_relative_to_file(base_file_path, relative_path):
    base_dir = os.path.dirname(os.path.abspath(base_file_path))
    return os.path.normpath(os.path.join(base_dir, relative_path))

def score_games():
    scored = ScoringValues.objects.get(id = 1)
    last_scored = scored.last_scored.replace(tzinfo=None)
    test_time = datetime.datetime.now() + datetime.timedelta(minutes=-5)
    if last_scored < test_time:
        scored.last_scored = datetime.datetime.now().replace(tzinfo=pytz.utc)
        scored.save()
        brackets = Brackets.objects.all()
        games = Games.objects.all()
        scores = ScoringValues.objects.all()
        teams = Teams.objects.all()
        for x in teams.values():
            team = Teams.objects.get(id=x['id'])
            team.picks_to_win = 0
            team.save()
        for x in brackets.values():
            score = 0
            best_score = 0
            bracket = Brackets.objects.get(id=x['id'])
            for y in games:
                bracket_game = "game" + str(y.id)
                if y.game_winner !=0:
                    if x[bracket_game] == y.game_winner:
                        for z in scores.values():
                            for c in teams.values():
                                if c['team_seed'] == z['seed'] and c['id'] == y.game_winner:
                                    for a in range(1,8):
                                        b = "r{}".format(a)
                                        if a == y.game_round_id:
                                            score += z[b]
                else:
                    for z in scores.values():
                        for c in teams.values():
                            if c['team_seed'] == z['seed'] and c['id'] == x[bracket_game]:
                                for a in range(1,8):
                                    b = "r{}".format(a)
                                    if a == y.game_round_id:
                                        best_score += z[b]

            best_score += score

            bracket.total_score = score
            bracket.best = best_score
            bracket.save()
            if bracket_game == "game67":
                team_winner = Teams.objects.get(id=x[bracket_game])
                team_winner.picks_to_win += 1
                team_winner.save()
        prev_score = 0
        prev_rank = 1
        for p in Brackets.objects.raw('SELECT @rowNum := @rowNum +1 as myrow, id, total_score FROM `march_madness_brackets`, (select @rownum :=0) as r order by total_score DESC'):
            bracket = Brackets.objects.get(id=p.id)
            if p.total_score == prev_score:
                bracket.rank = prev_rank
            else:
                bracket.rank = p.myrow
                prev_score = p.total_score
                prev_rank = p.rank
            bracket.save()

def get_teams(games, teams, regions):
    ff = []
    r64 = []
    region = {}
    for x in games:
        for z in regions:
            if x.game_round_id == 1:
                if x.game_region_id == z.id:
                    for y in teams:
                        if x.hteam == y.id:
                            hteam_name = y.team_name
                            hteam_seed = y.team_seed
                            region[z.id] = y.team_seed
                            region_name = z.region_name
                        if x.vteam == y.id:
                            vteam_name = y.team_name
                            vteam_seed = y.team_seed
                    ff.append([x.id,hteam_seed,hteam_name,vteam_seed, vteam_name,x.win_game_id,x.game_region_id,region_name])
            elif x.game_round_id == 2:
                if x.game_region_id == z.id:
                    for y in teams:
                        if x.hteam == y.id:
                            hteam_name = y.team_name
                            hteam_seed = y.team_seed
                            region_name = z.region_name
                        elif x.hteam == 0:
                            hteam_name = 'Winner of First Four Game'
                            hteam_seed = region[z.id]
                            region_name = z.region_name
                        if x.vteam == y.id:
                            vteam_name = y.team_name
                            vteam_seed = y.team_seed
                        elif x.vteam == 0:
                            vteam_name = 'Winner of First Four Game'
                            vteam_seed = region[z.id]
                    r64.append([x.id,hteam_seed,hteam_name,vteam_seed, vteam_name,x.win_game_id, x.game_region_id, region_name])
    return ff, r64

def home_or_away(seed):
    if seed > 8:
        win_home = 1
    else:
        win_home = 0
    return win_home
    
def truncate_table(table):
    sql = "Truncate table march_madness_{}".format(table)
    cursor = connection.cursor()
    cursor.execute(sql)

def create_teams(game_1_hteam_seed, game_1_hteam_name, game_1_vteam_seed, game_1_vteam_name, game_2_hteam_seed, game_2_hteam_name, game_2_vteam_seed, game_2_vteam_name, game_3_hteam_seed, game_3_hteam_name, game_3_vteam_seed, game_3_vteam_name, game_4_hteam_seed, game_4_hteam_name, game_4_vteam_seed, game_4_vteam_name):
    for x in range (1,69):
        team = Teams()
        if x < 3 and x % 2 == 0:
            team.team_seed = game_1_vteam_seed
            team.team_name = game_1_vteam_name
            team.team_region_id = 1
            team.picks_to_win = 0
        elif x < 3 :
            team.team_seed = game_1_hteam_seed
            team.team_name = game_1_hteam_name
            team.team_region_id = 1
            team.picks_to_win = 0
        elif x < 5 and x % 2 == 0:
            team.team_seed = game_2_vteam_seed
            team.team_name = game_2_vteam_name
            team.team_region_id = 2
            team.picks_to_win = 0
        elif x < 5:
            team.team_seed = game_2_hteam_seed
            team.team_name = game_2_hteam_name
            team.team_region_id = 2
            team.picks_to_win = 0
        elif x < 7 and x % 2 == 0:
            team.team_seed = game_3_vteam_seed
            team.team_name = game_3_vteam_name
            team.team_region_id = 3
            team.picks_to_win = 0
        elif x < 7:
            team.team_seed = game_3_hteam_seed
            team.team_name = game_3_hteam_name
            team.team_region_id = 3
            team.picks_to_win = 0
        elif x < 9 and x % 2 == 0:
            team.team_seed = game_4_vteam_seed
            team.team_name = game_4_vteam_name
            team.team_region_id = 4
            team.picks_to_win = 0
        elif x < 9:
            team.team_seed = game_4_hteam_seed
            team.team_name = game_4_hteam_name
            team.team_region_id = 4
            team.picks_to_win = 0
        elif x < 24:
            team.team_seed = 0
            team.team_name = ""
            team.team_region_id = 1
            team.picks_to_win = 0
        elif x < 39:
            team.team_seed = 0
            team.team_name = ""
            team.team_region_id = 3
            team.picks_to_win = 0
        elif x < 54:
            team.team_seed = 0
            team.team_name = ""
            team.team_region_id = 2
            team.picks_to_win = 0
        else:
            team.team_seed = 0
            team.team_name = ""
            team.team_region_id = 4
            team.picks_to_win = 0
        team.save()

def create_games(game_1_win_game, game_1_seed, game_2_win_game, game_2_seed, game_3_win_game, game_3_seed, game_4_win_game, game_4_seed):
    win_game = 37
    team_id = 9
    win_from = 5
    for x in range (1,68):
        game = Games()
        game.game_winner = 0
        if x < 5:
            game.game_round_id = 1
            if x == 1:
                game.hteam = 1
                game.vteam = 2
                game.win_game_id = game_1_win_game
                if game_1_seed < 9:
                    game.win_home = 0
                else:
                    game.win_home = 1
                game.game_region_id = 1
                game.game_winner = 0
                game.hteam_from = 0
                game.vteam_from = 0
            elif x == 2:
                game.hteam = 3
                game.vteam = 4
                game.win_game_id = game_2_win_game
                if game_2_seed < 9:
                    game.win_home = 0
                else:
                    game.win_home = 1
                game.game_region_id = 2
                game.game_winner = 0
                game.hteam_from = 0
                game.vteam_from = 0
            elif x == 3:
                game.hteam = 5
                game.vteam = 6
                game.win_game_id = game_3_win_game
                if game_3_seed < 9:
                    game.win_home = 0
                else:
                    game.win_home = 1
                game.game_region_id = 3
                game.game_winner = 0
                game.hteam_from = 0
                game.vteam_from = 0
            elif x == 4:
                game.hteam = 7
                game.vteam = 8
                game.win_game_id = game_4_win_game
                if game_4_seed < 9:
                    game.win_home = 0
                else:
                    game.win_home = 1
                game.game_region_id = 4
                game.game_winner = 0
                game.hteam_from = 0
                game.vteam_from = 0
        elif x < 37:
            game.game_round_id = 2
            if x % 2 == 0:
                game.win_game_id = win_game
                win_game += 1
                game.win_home = 1
            else:
                game.win_game_id = win_game
                game.win_home = 0
            if x == int(game_1_win_game):
                if game_1_seed < 9:
                    game.hteam = 0
                    game.hteam_from = 1
                    game.vteam = team_id
                    game.vteam_from = 0
                    team_id += 1
                else:
                    game.vteam = 0
                    game.vteam_from = 1
                    game.hteam = team_id
                    game.hteam_from = 0
                    team_id += 1
            elif x == int(game_2_win_game):
                if game_2_seed < 9:
                    game.hteam = 0
                    game.hteam_from = 1
                    game.vteam = team_id
                    game.vteam_from = 0
                    team_id += 1
                else:
                    game.vteam = 0
                    game.vteam_from = 1
                    game.hteam = team_id
                    game.hteam_from = 0
                    team_id += 1
            elif x == int(game_3_win_game):
                if game_3_seed < 9:
                    game.hteam = 0
                    game.hteam_from = 1
                    game.vteam = team_id
                    game.vteam_from = 0
                    team_id += 1
                else:
                    game.vteam = 0
                    game.vteam_from = 1
                    game.hteam = team_id
                    game.hteam_from = 0
                    team_id += 1
            elif x == int(game_4_win_game):
                if game_4_seed < 9:
                    game.hteam = 0
                    game.hteam_from = 1
                    game.vteam = team_id
                    game.vteam_from = 0
                    team_id += 1
                else:
                    game.vteam = 0
                    game.vteam_from = 1
                    game.hteam = team_id
                    game.hteam_from = 0
                    team_id += 1
            else:
                game.hteam = team_id
                game.hteam_from = 0
                team_id += 1
                game.vteam = team_id
                game.vteam_from = 0
                team_id += 1
            if x < 13:
                game.game_region_id = 1
            elif x < 21:
                game.game_region_id = 3
            elif x < 29:
                game.game_region_id = 2
            elif x < 37:
                game.game_region_id = 4
        elif x < 53:
            game.game_round_id = 3
            game.hteam = 0
            game.vteam = 0
            game.hteam_from = win_from
            win_from += 1
            game.vteam_from = win_from
            win_from += 1
            if x % 2 == 0:
                game.win_game_id = win_game
                win_game += 1
                game.win_home = 1
            else:
                game.win_game_id = win_game
                game.win_home = 0
            if x < 41:
                game.game_region_id = 1
            elif x < 45:
                game.game_region_id = 3
            elif x < 49:
                game.game_region_id = 2
            elif x < 53:
                game.game_region_id = 4
        elif x < 61:
            game.game_round_id = 4
            game.hteam = 0
            game.vteam = 0
            game.hteam_from = win_from
            win_from += 1
            game.vteam_from = win_from
            win_from += 1
            if x % 2 == 0:
                game.win_game_id = win_game
                win_game += 1
                game.win_home = 1
            else:
                game.win_game_id = win_game
                game.win_home = 0
            if x < 55:
                game.game_region_id = 1
            elif x < 57:
                game.game_region_id = 3
            elif x < 59:
                game.game_region_id = 2
            elif x < 61:
                game.game_region_id = 4
        elif x < 65:
            game.game_round_id = 5
            game.hteam = 0
            game.vteam = 0
            game.hteam_from = win_from
            win_from += 1
            game.vteam_from = win_from
            win_from += 1
            if x % 2 == 0:
                game.win_game_id = win_game
                win_game += 1
                game.win_home = 1
            else:
                game.win_game_id = win_game
                game.win_home = 0
            if x < 62:
                game.game_region_id = 1
            elif x < 63:
                game.game_region_id = 3
            elif x < 64:
                game.game_region_id = 2
            elif x < 65:
                game.game_region_id = 4
        elif x < 67:
            game.game_round_id = 6
            game.hteam = 0
            game.vteam = 0
            game.hteam_from = win_from
            win_from += 1
            game.vteam_from = win_from
            win_from += 1
            if x % 2 == 0:
                game.win_game_id = win_game
                win_game += 1
                game.win_home = 1
            else:
                game.win_game_id = win_game
                game.win_home = 0
            if x < 66:
                game.game_region_id = 1
            elif x < 67:
                game.game_region_id = 2
        else:
            game.game_round_id = 7
            game.hteam = 0
            game.vteam = 0
            game.hteam_from = win_from
            win_from += 1
            game.vteam_from = win_from
            win_from += 1
            game.win_home = 0
            game.game_region_id = 1
            game.win_game_id = 67
        game.save()

def site_test():
    site_test = 0
    teams = Teams.objects.all()
    for x in teams:
        if x.team_seed == 0:
            site_test += 1
    if site_test == 0:
        site = Site.objects.get(id=1)
        site.bracket_setup = True
        site.save()

# Create your views here.
def index(request):
    if request.user.is_superuser == 1:
        admin = 1
    else:
        admin = 0
    if request.POST:
        pass
    else:
        context = RequestContext(request)
        template_name = 'march_madness/index.html'
        blog_list = Blog.objects.all()
        score_games()
        site = Site.objects.all()
        teams = Teams.objects.order_by('-picks_to_win')
        stats = []
        for x in teams.values():
            total = len(Brackets.objects.all())
            if x['picks_to_win'] > 0:
                percent = x['picks_to_win'] / float(total) * 100
                stats.append([x['team_name'], percent])

        if not request.user.is_authenticated():
            brackets = []
        else:
            brackets = Brackets.objects.filter(user_id = request.user.id).order_by('rank')

        standings = Brackets.objects.order_by('rank')
        cur_standings = []
        print_standings = []
        for x in standings.values():
            if x['rank'] < 10:
                cur_standings.append([x['name'], x['total_score'], x['rank']])
        if len(cur_standings) > 10:
            length = len(cur_standings) - 1
            last_rank = cur_standings[length][2]
            last_score = cur_standings[length][1]
            for x in cur_standings:
                if x[2] != last_rank:
                    print_standings.append(x)
            if len(print_standings) != len(cur_standings):
                tied = len(cur_standings) - len(print_standings)
                tied = str(tied)
                tied = "{} brackets tied at".format(tied)
                print_standings.append([tied, last_score, last_rank])
        else:
            for x in cur_standings:
                print_standings.append(x)

        users = len(set(Brackets.objects.order_by('user_id').values_list('user_id', flat=True)))
        total_brackets = len(Brackets.objects.all())
        smacktalk_len = len(SmackTalk.objects.all())
        if smacktalk_len == 0:
            smacktalk = smacktalk_len
        else:
            smacktalk = SmackTalk.objects.all()
        context_dict = {
        'blogs': blog_list,
        'brackets' : brackets,
        'standings' : print_standings,
        'stats': stats,
        'users': users,
        'total_brackets': total_brackets,
        'smacktalk': smacktalk,
        'site': site,
        'admin': admin
        }

        return render_to_response(template_name, context_dict, context)

def create(request):
    if not request.user.is_authenticated():
        return redirect('/register/?next=%s' % (request.path))
    if request.user.is_superuser == 1:
        admin = 1
    else:
        admin = 0
    if request.POST:
        context = RequestContext(request)
        form = request.POST
        bracket = Brackets()
        bracket.name = request.POST['bracket_name']
        bracket.tiebreaker = request.POST['tiebreak_range']
        bracket.game1 = request.POST['game1']
        bracket.game2 = request.POST['game2']
        bracket.game3 = request.POST['game3']
        bracket.game4 = request.POST['game4']
        bracket.game5 = request.POST['game5']
        bracket.game6 = request.POST['game6']
        bracket.game7 = request.POST['game7']
        bracket.game8 = request.POST['game8']
        bracket.game9 = request.POST['game9']
        bracket.game10 = request.POST['game10']
        bracket.game11 = request.POST['game11']
        bracket.game12 = request.POST['game12']
        bracket.game13 = request.POST['game13']
        bracket.game14 = request.POST['game14']
        bracket.game15 = request.POST['game15']
        bracket.game16 = request.POST['game16']
        bracket.game17 = request.POST['game17']
        bracket.game18 = request.POST['game18']
        bracket.game19 = request.POST['game19']
        bracket.game20 = request.POST['game20']
        bracket.game21 = request.POST['game21']
        bracket.game22 = request.POST['game22']
        bracket.game23 = request.POST['game23']
        bracket.game24 = request.POST['game24']
        bracket.game25 = request.POST['game25']
        bracket.game26 = request.POST['game26']
        bracket.game27 = request.POST['game27']
        bracket.game28 = request.POST['game28']
        bracket.game29 = request.POST['game29']
        bracket.game30 = request.POST['game30']
        bracket.game31 = request.POST['game31']
        bracket.game32 = request.POST['game32']
        bracket.game33 = request.POST['game33']
        bracket.game34 = request.POST['game34']
        bracket.game35 = request.POST['game35']
        bracket.game36 = request.POST['game36']
        bracket.game37 = request.POST['game37']
        bracket.game38 = request.POST['game38']
        bracket.game39 = request.POST['game39']
        bracket.game40 = request.POST['game40']
        bracket.game41 = request.POST['game41']
        bracket.game42 = request.POST['game42']
        bracket.game43 = request.POST['game43']
        bracket.game44 = request.POST['game44']
        bracket.game45 = request.POST['game45']
        bracket.game46 = request.POST['game46']
        bracket.game47 = request.POST['game47']
        bracket.game48 = request.POST['game48']
        bracket.game49 = request.POST['game49']
        bracket.game50 = request.POST['game50']
        bracket.game51 = request.POST['game51']
        bracket.game52 = request.POST['game52']
        bracket.game53 = request.POST['game53']
        bracket.game54 = request.POST['game54']
        bracket.game55 = request.POST['game55']
        bracket.game56 = request.POST['game56']
        bracket.game57 = request.POST['game57']
        bracket.game58 = request.POST['game58']
        bracket.game59 = request.POST['game59']
        bracket.game60 = request.POST['game60']
        bracket.game61 = request.POST['game61']
        bracket.game62 = request.POST['game62']
        bracket.game63 = request.POST['game63']
        bracket.game64 = request.POST['game64']
        bracket.game65 = request.POST['game65']
        bracket.game66 = request.POST['game66']
        bracket.game67 = request.POST['game67']
        bracket.user_id = request.user
        bracket.total_score = 0
        bracket.save()
        bracket_id = str(bracket.id)
        pdf_name, pdf_loc  = getPdf( bracket.id, request.user.username)
        name = "%s %s" % (request.user.first_name, request.user.last_name)
        send_email = emailPdf(name , request.user.email, pdf_loc)
        context_dict = {
            'pdf_link': pdf_name,
            'bracket_name': bracket.name,
            'bracket_id': bracket_id,
            'id': 'create',
            'admin': admin
        }
        return render_to_response('march_madness/submitted.html', context_dict, context)
    else:
        context = RequestContext(request)
        current_user = request.user

        template_name = 'march_madness/create_bracket.html'
        game_list = Games.objects.all()
        round_list = Rounds.objects.all()
        region_list = Regions.objects.all()
        team_list = Teams.objects.all()
        first_four = getFirstFour(game_list, team_list)
        round_1_region_1 = getRoundGames(game_list, team_list, 2, 1)
        round_1_region_2 = getRoundGames(game_list, team_list, 2, 2)
        round_1_region_3 = getRoundGames(game_list, team_list, 2, 3)
        round_1_region_4 = getRoundGames(game_list, team_list, 2, 4)
        round_2_region_1 = getRoundGames(game_list, team_list, 3, 1)
        round_2_region_2 = getRoundGames(game_list, team_list, 3, 2)
        round_2_region_3 = getRoundGames(game_list, team_list, 3, 3)
        round_2_region_4 = getRoundGames(game_list, team_list, 3, 4)
        round_3_region_1 = getRoundGames(game_list, team_list, 4, 1)
        round_3_region_2 = getRoundGames(game_list, team_list, 4, 2)
        round_3_region_3 = getRoundGames(game_list, team_list, 4, 3)
        round_3_region_4 = getRoundGames(game_list, team_list, 4, 4)
        round_4_region_1 = getRoundGames(game_list, team_list, 5, 1)
        round_4_region_2 = getRoundGames(game_list, team_list, 5, 2)
        round_4_region_3 = getRoundGames(game_list, team_list, 5, 3)
        round_4_region_4 = getRoundGames(game_list, team_list, 5, 4)
        round_5_region_1 = getRoundGames(game_list, team_list, 6, 1)
        round_5_region_2 = getRoundGames(game_list, team_list, 6, 2)
        round_6_region_1 = getRoundGames(game_list, team_list, 7, 1)
        round_6_region_2 = getRoundGames(game_list, team_list, 7, 2)
        round_7_region_1 = getRoundGames(game_list, team_list, 8, 1)
        site = Site.objects.all()
        context_dict = {
            'context': context,
            'first_four': first_four,
            'round1_region1': round_1_region_1,
            'round1_region2': round_1_region_2,
            'round1_region3': round_1_region_3,
            'round1_region4': round_1_region_4,
            'round2_region1': round_2_region_1,
            'round2_region2': round_2_region_2,
            'round2_region3': round_2_region_3,
            'round2_region4': round_2_region_4,
            'round3_region1': round_3_region_1,
            'round3_region2': round_3_region_2,
            'round3_region3': round_3_region_3,
            'round3_region4': round_3_region_4,
            'round4_region1': round_4_region_1,
            'round4_region2': round_4_region_2,
            'round4_region3': round_4_region_3,
            'round4_region4': round_4_region_4,
            'round5_region1': round_5_region_1,
            'round5_region2': round_5_region_2,
            'round6_region1': round_6_region_1,
            'round6_region2': round_6_region_2,
            'round7_region1': round_7_region_1,
            'regions': region_list,
            'site': site,
            'admin': admin
        }
        return render_to_response(template_name, context_dict, context)

def register(request):
    if request.user.is_superuser == 1:
        admin = 1
    else:
        admin = 0
    context = RequestContext(request)
    template_name = 'march_madness/register.html'
    site = Site.objects.all()
    if request.method == 'GET':
        context = RequestContext(request)
        template_name = 'march_madness/register.html'
        form = POSTForm()
        site = Site.objects.all()
        context_dict = {
            'form': form,
            'site': site,
            'admin': admin
        }

    else:
        form = POSTForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            first = form.cleaned_data['first_name']
            last = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            context_dict = {
            }
            user = User.objects.create_user( username, email, password)
            user.first_name = first
            user.last_name = last
            user.is_active = 1
            user.is_staff = 1
            user.save()
            un = username
            pw = password
            user = authenticate(username=un, password=pw)
            if user is not None:
                if user.is_active:
                    login(request, user)
                else:
                    #Retuen disabled account error
                    pass
            else:
                #Return invalid login error
                pass

            return redirect('/create')
        else:
            context_dict = {
                'form' : form,
                'form_data': "Form is not valid",
                'site': site,
                'admin': admin
            }
    return render_to_response(template_name, context_dict, context)

def logout_view(request):
    logout(request)
    return redirect('/')

def printout(request):
   # Create the HttpResponse object with the appropriate PDF headers.
    bracket_id = request.GET['id']
    bracket_set = Brackets.objects.filter(id = bracket_id).values()
    bracket_name = bracket_set[0]['name']
    save_name = request.user.username + "_" + bracket_name + ".pdf"
    full_name =  "/media/" +  save_name
    file_name = "'attachment; filename=" + full_name
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = file_name

    return response

def edit(request):
    if request.user.is_superuser == 1:
        admin = 1
    else:
        admin = 0
    context = RequestContext(request)
    template_name = 'march_madness/edit.html'
    site = Site.objects.all()

    if request.method == "GET":
        bracket_id = request.GET['id']
        teams = Teams.objects.all()
        games = Games.objects.all()
        bracket = Brackets.objects.get(id = bracket_id)
        region_list = Regions.objects.all()
        first_four, round_1_region_1, round_1_region_2, round_1_region_3, round_1_region_4, round_2_region_1, round_2_region_2, round_2_region_3, round_2_region_4, round_3_region_1, round_3_region_2, round_3_region_3, round_3_region_4, round_4_region_1, round_4_region_2, round_4_region_3, round_4_region_4, round_5_region_1, round_5_region_2, round_6_region_1, round_7_region_1 = get_bracket(bracket_id, games, teams)
        user_id = request.user
        bracket_id = bracket.user_id

        if bracket.user_id == request.user:
            auth = 0
        else:
            auth = 1

        context_dict= {
            'games' : games,
            'first_four': first_four,
            'round1_region1': round_1_region_1,
            'round1_region2': round_1_region_2,
            'round1_region3': round_1_region_3,
            'round1_region4': round_1_region_4,
            'round2_region1': round_2_region_1,
            'round2_region2': round_2_region_2,
            'round2_region3': round_2_region_3,
            'round2_region4': round_2_region_4,
            'round3_region1': round_3_region_1,
            'round3_region2': round_3_region_2,
            'round3_region3': round_3_region_3,
            'round3_region4': round_3_region_4,
            'round4_region1': round_4_region_1,
            'round4_region2': round_4_region_2,
            'round4_region3': round_4_region_3,
            'round4_region4': round_4_region_4,
            'round5_region1': round_5_region_1,
            'round5_region2': round_5_region_2,
            'round6_region1': round_6_region_1,
            'round7_region1': round_7_region_1,
            'regions': region_list,
            'bracket': bracket,
            'auth': auth,
            'user_id': user_id,
            'bracket_id': bracket_id,
            'site': site,
            'admin': admin
        }
        return render_to_response(template_name, context_dict, context)
    else:
        bracket_id = request.POST['id']
        bracket = Brackets.objects.get(id = bracket_id)
        bracket.tiebreaker = request.POST['tiebreak_range']
        bracket.game1 = request.POST['game1']
        bracket.game2 = request.POST['game2']
        bracket.game3 = request.POST['game3']
        bracket.game4 = request.POST['game4']
        bracket.game5 = request.POST['game5']
        bracket.game6 = request.POST['game6']
        bracket.game7 = request.POST['game7']
        bracket.game8 = request.POST['game8']
        bracket.game9 = request.POST['game9']
        bracket.game10 = request.POST['game10']
        bracket.game11 = request.POST['game11']
        bracket.game12 = request.POST['game12']
        bracket.game13 = request.POST['game13']
        bracket.game14 = request.POST['game14']
        bracket.game15 = request.POST['game15']
        bracket.game16 = request.POST['game16']
        bracket.game17 = request.POST['game17']
        bracket.game18 = request.POST['game18']
        bracket.game19 = request.POST['game19']
        bracket.game20 = request.POST['game20']
        bracket.game21 = request.POST['game21']
        bracket.game22 = request.POST['game22']
        bracket.game23 = request.POST['game23']
        bracket.game24 = request.POST['game24']
        bracket.game25 = request.POST['game25']
        bracket.game26 = request.POST['game26']
        bracket.game27 = request.POST['game27']
        bracket.game28 = request.POST['game28']
        bracket.game29 = request.POST['game29']
        bracket.game30 = request.POST['game30']
        bracket.game31 = request.POST['game31']
        bracket.game32 = request.POST['game32']
        bracket.game33 = request.POST['game33']
        bracket.game34 = request.POST['game34']
        bracket.game35 = request.POST['game35']
        bracket.game36 = request.POST['game36']
        bracket.game37 = request.POST['game37']
        bracket.game38 = request.POST['game38']
        bracket.game39 = request.POST['game39']
        bracket.game40 = request.POST['game40']
        bracket.game41 = request.POST['game41']
        bracket.game42 = request.POST['game42']
        bracket.game43 = request.POST['game43']
        bracket.game44 = request.POST['game44']
        bracket.game45 = request.POST['game45']
        bracket.game46 = request.POST['game46']
        bracket.game47 = request.POST['game47']
        bracket.game48 = request.POST['game48']
        bracket.game49 = request.POST['game49']
        bracket.game50 = request.POST['game50']
        bracket.game51 = request.POST['game51']
        bracket.game52 = request.POST['game52']
        bracket.game53 = request.POST['game53']
        bracket.game54 = request.POST['game54']
        bracket.game55 = request.POST['game55']
        bracket.game56 = request.POST['game56']
        bracket.game57 = request.POST['game57']
        bracket.game58 = request.POST['game58']
        bracket.game59 = request.POST['game59']
        bracket.game60 = request.POST['game60']
        bracket.game61 = request.POST['game61']
        bracket.game62 = request.POST['game62']
        bracket.game63 = request.POST['game63']
        bracket.game64 = request.POST['game64']
        bracket.game65 = request.POST['game65']
        bracket.game66 = request.POST['game66']
        bracket.game67 = request.POST['game67']
        bracket.user_id = request.user
        bracket.total_score = 0
        bracket.save()
        bracket_id = str(bracket.id)
        pdf_name, pdf_loc  = getPdf( bracket.id, request.user.username)
        name = "%s %s" % (request.user.first_name, request.user.last_name)
        send_email = emailPdf(name , request.user.email, pdf_loc)

        context_dict = {
            'pdf_link': pdf_name,
            'bracket_name': bracket.name,
            'bracket_id': bracket_id,
            'id': 'edit',
            'site': site,
            'admin': admin
        }
        return render_to_response('march_madness/submitted.html', context_dict, context)

def rules(request):
    if request.user.is_superuser == 1:
        admin = 1
    else:
        admin = 0
    context = RequestContext(request)
    template_name = 'march_madness/rules.html'
    scores = ScoringValues.objects.all()
    rounds = Rounds.objects.all()
    rules = Rules.objects.all()
    site = Site.objects.all()

    context_dict = {
        'scoring': scores,
        'rounds': rounds,
        'rules': rules,
        'site': site,
        'admin': admin
    }
    return render_to_response(template_name, context_dict, context)


def admin(request):
    if request.user.is_superuser != 1:
        return redirect ('/')
    context = RequestContext(request)
    template_name = 'march_madness/admin.html'
    site = Site.objects.get(id=1)
    regions = Regions.objects.all()
    games = Games.objects.all()
    teams = Teams.objects.all()
    if site.bracket_setup == True:
        ff, r64 = get_teams(games, teams, regions)
    else:
        if len(games) > 0 and len(teams) > 0 and len(regions) > 0:
            ff, r64 = get_teams(games, teams, regions)
        else:
            r64 = []
            ff = []
    site = Site.objects.all()
    rules = Rules.objects.all()
    seeds = []
    for x in range(1,17):
        seeds.append(x)
    context_dict = {
        'regions': regions,
        'site': site,
        'ff': ff,
        'r64': r64,
	'rules': rules,
        'seeds': seeds,
        'admin': 1,
    }
    return render_to_response(template_name, context_dict, context)

def update_site(request):
    if request.method == 'POST':
        response = {}
        site_name = request.POST['site_name']
        sweet_16 = request.POST.get('sweet_16', 0);
        region_1 = request.POST['region_1']
        region_2 = request.POST['region_2']
        region_3 = request.POST['region_3']
        region_4 = request.POST['region_4']
        site = Site.objects.all()
        if len(site) > 0 :
            site = Site.objects.get(id=1)
            site.name = site_name
            site.sweet_16 = sweet_16
        else:
            site = Site(name=site_name, sweet_16=sweet_16)
        site.save()
        response['result'] = 1
        response['site_name'] = site.name
        response['sweet_16'] = site.sweet_16
        regions = Regions.objects.all()
        if len(regions) > 0:
            for x in regions:
                region = "region_{}".format(x.id)
                update_region = Regions.objects.get(id=x.id)
                update_region.region_name = request.POST[region]
                update_region.save()
                response[region] = update_region.region_name
        else:
            region_1 = Regions(region_name=region_1)
            region_2 = Regions(region_name=region_2)
            region_3 = Regions(region_name=region_3)
            region_4 = Regions(region_name=region_4)
            region_1.save()
            region_2.save()
            region_3.save()
            region_4.save()
            response['region_1'] = region_1.region_name
            response['region_2'] = region_2.region_name
            response['region_3'] = region_3.region_name
            response['region_4'] = region_4.region_name
        return JsonResponse(response)
    else:
        response['result'] = 0
        return HttpResponse(
            response,
            content_type="application/html"
        )

def update_ff(request):
    response = {}
    if request.method == 'POST':
        site = Site.objects.get(id=1)
        if site.bracket_setup == True:
            games = Games.objects.order_by('id')[:4]
            for x in games:
                hteam_name = "game_{}_hteam_name".format(x.id)
                vteam_name = "game_{}_vteam_name".format(x.id)
                win_game = "game_{}_win_game".format(x.id)
                game = Games.objects.get(id = x.id)
                hteam = Teams.objects.get(id = x.hteam)
                vteam = Teams.objects.get(id = x.vteam)
                game.win_game_id = request.POST[win_game]
                hteam.team_name = request.POST[hteam_name]
                vteam.team_name = request.POST[vteam_name]
                hteam.save()
                vteam.save()
                game.save()
            response['game'] = 'updated'

        else:
            # Initialize Games and Teams
            game_1_hteam_seed = request.POST['game_1_hteam_seed']
            game_1_hteam_name = request.POST['game_1_hteam_name']
            game_1_vteam_seed = request.POST['game_1_vteam_seed']
            game_1_vteam_name = request.POST['game_1_vteam_name']
            game_1_win_game = request.POST['game_1_win_game']
            game_2_hteam_seed = request.POST['game_2_hteam_seed']
            game_2_hteam_name = request.POST['game_2_hteam_name']
            game_2_vteam_seed = request.POST['game_2_vteam_seed']
            game_2_vteam_name = request.POST['game_2_vteam_name']
            game_2_win_game = request.POST['game_2_win_game']
            game_3_hteam_seed = request.POST['game_3_hteam_seed']
            game_3_hteam_name = request.POST['game_3_hteam_name']
            game_3_vteam_seed = request.POST['game_3_vteam_seed']
            game_3_vteam_name = request.POST['game_3_vteam_name']
            game_3_win_game = request.POST['game_3_win_game']
            game_4_hteam_seed = request.POST['game_4_hteam_seed']
            game_4_hteam_name = request.POST['game_4_hteam_name']
            game_4_vteam_seed = request.POST['game_4_vteam_seed']
            game_4_vteam_name = request.POST['game_4_vteam_name']
            game_4_win_game = request.POST['game_4_win_game']
            # Make sure tables are clean before starting
            truncate_table('games')
            truncate_table('teams')
            # Create Teams
            create_teams(game_1_hteam_seed, game_1_hteam_name, game_1_vteam_seed, game_1_vteam_name, game_2_hteam_seed, game_2_hteam_name, game_2_vteam_seed, game_2_vteam_name, game_3_hteam_seed, game_3_hteam_name, game_3_vteam_seed, game_3_vteam_name, game_4_hteam_seed, game_4_hteam_name, game_4_vteam_seed, game_4_vteam_name)
            # Create Games
            create_games(game_1_win_game, game_1_hteam_seed, game_2_win_game, game_2_hteam_seed, game_3_win_game, game_3_hteam_seed, game_4_win_game, game_4_hteam_seed)
            site_test()
            response['ff'] = 'Games and Teams Initialized'
        return JsonResponse(response)
    else:
        response = {'result': 'failed'}
        return HttpResponse( response, content_type="application/html")

def update_r64_r1(request):
    response = {}
    if request.method == 'POST':
        site = Site.objects.get(id=1)
        games = Games.objects.filter(id__gt=4)[:8]
        for x in games:
            hteam_name = "game_{}_hteam_name".format(x.id)
            vteam_name = "game_{}_vteam_name".format(x.id)
            hteam_seed = "game_{}_hteam_seed".format(x.id)
            vteam_seed = "game_{}_vteam_seed".format(x.id)
            if x.hteam != 0:
                hteam = Teams.objects.get(id = x.hteam)
                hteam.team_name = request.POST[hteam_name]
                if site.bracket_setup == False:
                    hteam.team_seed = request.POST[hteam_seed]
                hteam.save()
            if x.vteam != 0:
                vteam = Teams.objects.get(id = x.vteam)
                vteam.team_name = request.POST[vteam_name]
                if site.bracket_setup == False:
                    vteam.team_seed = request.POST[vteam_seed]
                vteam.save()
        response['region_1'] = 'updated'
        if site.bracket_setup == False:
            site_test()
            
        return JsonResponse(response)
    else:
        response = {'result': 'failed'}
        return HttpResponse( response, content_type="application/html")

def update_r64_r2(request):
    response = {}
    if request.method == 'POST':
        site = Site.objects.get(id=1)
        games = Games.objects.filter(id__gt=20)[:8]
        for x in games:
            hteam_name = "game_{}_hteam_name".format(x.id)
            vteam_name = "game_{}_vteam_name".format(x.id)
            hteam_seed = "game_{}_hteam_seed".format(x.id)
            vteam_seed = "game_{}_vteam_seed".format(x.id)
            if x.hteam != 0:
                hteam = Teams.objects.get(id = x.hteam)
                hteam.team_name = request.POST[hteam_name]
                if site.bracket_setup == False:
                    hteam.team_seed = request.POST[hteam_seed]
                hteam.save()
            if x.vteam != 0:
                vteam = Teams.objects.get(id = x.vteam)
                vteam.team_name = request.POST[vteam_name]
                if site.bracket_setup == False:
                    vteam.team_seed = request.POST[vteam_seed]
                vteam.save()
        response['region_1'] = 'updated'
        if site.bracket_setup == False:
            site_test()
        return JsonResponse(response)
    else:
        response = {'result': 'failed'}
        return HttpResponse( response, content_type="application/html")

def update_r64_r3(request):
    response = {}
    if request.method == 'POST':
        site = Site.objects.get(id=1)
        games = Games.objects.filter(id__gt=12)[:8]
        for x in games:
            hteam_name = "game_{}_hteam_name".format(x.id)
            vteam_name = "game_{}_vteam_name".format(x.id)
            hteam_seed = "game_{}_hteam_seed".format(x.id)
            vteam_seed = "game_{}_vteam_seed".format(x.id)
            if x.hteam != 0:
                hteam = Teams.objects.get(id = x.hteam)
                hteam.team_name = request.POST[hteam_name]
                if site.bracket_setup == False:
                    hteam.team_seed = request.POST[hteam_seed]
                hteam.save()
            if x.vteam != 0:
                vteam = Teams.objects.get(id = x.vteam)
                vteam.team_name = request.POST[vteam_name]
                if site.bracket_setup == False:
                    vteam.team_seed = request.POST[vteam_seed]
                vteam.save()
        response['region_1'] = 'updated'
        if site.bracket_setup == False:
            site_test()
        return JsonResponse(response)
    else:
        response = {'result': 'failed'}
        return HttpResponse( response, content_type="application/html")

def update_r64_r4(request):
    response = {}
    if request.method == 'POST':
        site = Site.objects.get(id=1)
        games = Games.objects.filter(id__gt=28)[:8]
        for x in games:
            hteam_name = "game_{}_hteam_name".format(x.id)
            vteam_name = "game_{}_vteam_name".format(x.id)
            hteam_seed = "game_{}_hteam_seed".format(x.id)
            vteam_seed = "game_{}_vteam_seed".format(x.id)
            if x.hteam != 0:
                hteam = Teams.objects.get(id = x.hteam)
                hteam.team_name = request.POST[hteam_name]
                if site.bracket_setup == False:
                    hteam.team_seed = request.POST[hteam_seed]
                hteam.save()
            if x.vteam != 0:
                vteam = Teams.objects.get(id = x.vteam)
                vteam.team_name = request.POST[vteam_name]
                if site.bracket_setup == False:
                    vteam.team_seed = request.POST[vteam_seed]
                vteam.save()
        response['region_1'] = 'updated'
        if site.bracket_setup == False:
            site_test()
        return JsonResponse(response)
    else:
        response = {'result': 'failed'}
        return HttpResponse( response, content_type="application/html")

def update_rules_edit(request):
    response = {}
    if request.method == 'POST':
        rule_id = request.POST['edit_title']
        rule_title = request.POST['edit_title_name']
        rule_content = request.POST['edit_content']
        rule = Rules.objects.get(id=rule_id)
        rule.title = rule_title
        rule.content = rule_content
        rule.save()
        response['region_1'] = 'updated'
        return JsonResponse(response)
    else:
        response = {'result': 'failed'}
        return HttpResponse( response, content_type="application/html")

def update_rules_new(request):
    response = {}
    if request.method == 'POST':
        rule = Rules()
        rule.title = request.POST['new_title_name']
        rule.content = request.POST['new_content']
        rule.submission =  datetime.datetime.now().replace(tzinfo=pytz.utc)
        rule.save()
        response['new_id'] = rule.id
        response['new_title'] = rule.title
        response['region_1'] = 'updated'
        return JsonResponse(response)
    else:
        response = {'result': 'failed'}
        return HttpResponse( response, content_type="application/html")

def update_rules_edit_change(request):
    response = {}
    if request.method == 'POST':
	rule_id = request.POST['edit_title']
        rule = Rules.objects.get(id=rule_id)
        response['rule_id'] = rule.id
        response['rule_title'] = rule.title
        response['rule_content'] = rule.content
        response['region_1'] = 'updated'
        return JsonResponse(response)
    else:
        response = {'result': 'failed'}
        return HttpResponse( response, content_type="application/html")

def update_rules_del_change(request):
    response = {}
    if request.method == 'POST':
        rule_id = request.POST['del_title']
        rule = Rules.objects.get(id=rule_id)
        response['rule_id'] = rule.id
        response['rule_title'] = rule.title
        response['rule_content'] = rule.content
        response['region_1'] = 'updated'
        return JsonResponse(response)
    else:
        response = {'result': 'failed'}
        return HttpResponse( response, content_type="application/html")

def update_rules_del(request):
    response = {}
    if request.method == 'POST':
        rule_id = request.POST['del_title']
        rule = Rules.objects.get(id=rule_id)
        rule.delete()
        rule = Rules.objects.get(id=1)
        response['rule_id'] = rule_id
        response['rule_title'] = rule.title
        response['rule_content'] = rule.content
        response['region_1'] = 'updated'
        return JsonResponse(response)
    else:
        response = {'result': 'failed'}
        return HttpResponse( response, content_type="application/html")

