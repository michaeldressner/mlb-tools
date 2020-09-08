import csv
import sqlite3
from game import Game
from team import Team

conn = sqlite3.connect('lahmansbaseballdb.sqlite')
cursor = conn.cursor()

def search(cond, streak = False):
    teams = dict()
    team_states = dict()

    teamid_file = open('TEAMABR.TXT', 'r')
    for line in teamid_file:
        fields = line[:-1].split(',')
        fields = [field.strip('"') for field in fields]
        
        # https://www.retrosheet.org/TEAMABR.TXT
        abr = fields[0]
        league = fields[1]
        city = fields[2]
        nickname = fields[3]
        first_year = fields[4]
        last_year = fields[5]
        teams[abr] = Team(abr, league, city, nickname, first_year, last_year)
    teamid_file.close()

    stats = ['ab', 'h', 'd', 't', 'hr', 'rbi', 'sh', 'sf', 'hbp', 'w', 'iw',
            'so', 'sb', 'cs', 'gidp', 'ci', 'lob', 'pu', 'ier', 'er', 'wp',
            'bk', 'po', 'ass', 'err', 'pb', 'dp', 'tp']
    for year in range(2008, 2020):
        gl_file = open('gl/GL' + str(year) + '.TXT', 'r')
        for line in csv.reader(gl_file, delimiter = ","):
            game = Game(line)

            # Let's assume condition has the stat name, then an operator,
            # then a value
            # Ex: h > 4, hr >= 4
            tokens = cond.split()
            cond_stat = tokens[0]
            cond_op = tokens[1]
            cond_val = tokens[2]

            if streak:
                pass
            else:
                if eval('getattr(game, \'v_' + cond_stat + '\') ' + cond_op +
                        cond_val) or eval('getattr(game, \'h_' + cond_stat +
                                '\') ' + cond_op + cond_val):
                    print(game.date + " " + game.v_team + "@" + game.h_team)

            for stat in stats:
                teams[game.v_team].add_stat(stat, getattr(game, 'v_' + stat))
                teams[game.h_team].add_stat(stat, getattr(game, 'h_' + stat))

        gl_file.close()

search("iw > 4")
