#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 16:39:04 2021

@author: Robinson Montes
"""
from flask import Flask, jsonify, make_response
import MySQLdb

app = Flask(__name__)


@app.errorhandler(400)
def not_understand(error):
    """
    Error handler funtion when the server could not understand the request due
    to invalid syntax.

    Returns:
        Bad Request with a status code 400.
    """
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    """
    Error handler funtion when The server can not find the requested resource.
    The URL is not recognized.

    Returns:
        Not Found with a status code 400.
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/')
@app.route('/GetPlayerStats')
@app.route('/GetPlayerStats/<int:player_id>')
def GetPlayerStats(player_id: int = 1):
    """
    GetPlayerStats - given a player ID, display that player's stats.

    Returns:
        json: The API with player stats.
    """
    cursor = db.cursor()
    cursor.execute('SELECT players.fname, players.lname, stats.name, '
                   'stats.value '
                   'FROM players JOIN stats ON players.id=stats.player_id '
                   f'WHERE players.id={player_id};')
    rows = cursor.fetchall()
    if len(rows) != 0:
        data = {
            'id': player_id,
            'first name': rows[0][0],
            'last name': rows[0][1],
            'stats': {}
        }
        for row in rows:
            data['stats'][row[2]] = row[3]
    else:
        return jsonify({'player_id': 'Not Found'}), 204
    return jsonify(data), 200


@app.route('/GetTeamPlayers')
@app.route('/GetTeamPlayers/<int:team_id>')
def GetTeamPlayers(team_id: int = 1):
    """
    GetTeamPlayers - given a team ID, display all the stats for all the players
    on that team who had at least 2 touchdowns (TDs).

    Returns:
        json: The API with team stats.
    """
    cursor = db.cursor()
    cursor.execute('SELECT teams.name, teams.city, players.id, '
                   'players.fname, players.lname, stats.name, stats.value '
                   'FROM players JOIN stats ON players.id=stats.player_id '
                   'JOIN teams ON players.team_id = teams.id '
                   f'WHERE teams.id={team_id};')
    rows = cursor.fetchall()
    if len(rows) != 0:
        data = {
            'id': team_id,
            'team name': rows[0][0],
            'city': rows[0][1],
            'players': []
        }
        count = 0
        stats = {}
        for row in rows:
            count += 1
            stats[row[5]] = row[6]
            if count == 3:
                if stats['TDs'] >= 2:
                    data['players'].append({
                        'id': row[2],
                        'first name': row[3],
                        'last name': row[4],
                        'stats': stats
                        })
                stats = {}
                count = 0
    else:
        return jsonify({'Result': 'Not Found'}), 204
    return jsonify(data), 200


if __name__ == '__main__':
    db = MySQLdb.connect(host='localhost',
                         user='root',
                         passwd='2762',
                         db='testdb',
                         port=3306)
    app.run(debug=True, port=5000, host='localhost')
    db.close()

