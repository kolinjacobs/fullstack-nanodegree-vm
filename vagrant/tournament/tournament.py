#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=players")

def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("delete from matches;")
    c.execute("UPDATE players SET wins = 0, matches = 0")
    DB.commit()
    DB.close()
def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM players")
    DB.commit()
    c.close()

def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT count(*) FROM players")
    result = c.fetchone()
    number = result[0]
    #raise ValueError(number)
    return int(number)

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO players (id, player_name, wins, matches)"
              "VALUES (DEFAULT, %s, 0,0);",
              (name,))
    DB.commit()
    c.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT * FROM players ORDER BY wins DESC")
    players = []
    for row in c.fetchall():
        player = (int(row[0]),str(row[1]),int(row[2]),int(row[3]))
        players.append(player)
    DB.close()
    return players

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT * FROM players ORDER BY wins DESC")
    players = []
    winner_name = ""
    loser_name = ""
    for row in c.fetchall():
        player = (int(row[0]),str(row[1]),int(row[2]),int(row[3]))
        players.append(player)
        if int(row[0]) == winner:
            winner_name = str(row[1])
        if int(row[0]) == loser:
            loser_name = str(row[1])

    c.execute("UPDATE players SET wins = wins + 1, matches = matches + 1"
              "WHERE id = %s",
              (winner,))
    c.execute("UPDATE players SET matches = matches + 1"
              "WHERE id = %s",
              (loser,))
    c.execute("INSERT INTO matches (id_one, player_one, id_two, player_two, winner)"
              "VALUES (%s, %s, %s,%s,%s);",
              (winner, winner_name, loser, loser_name, winner))
    DB.commit()
    c.close()
    DB.commit()
    c.close()
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT * FROM players ORDER BY wins DESC")
    players = []
    for row in c.fetchall():
        player = (int(row[0]),str(row[1]),int(row[2]),int(row[3]))
        players.append(player)
    matches = []
    matches_number = int(len(players)/2)
    for x in range(0, matches_number):
        match = (int(players[x*2][0]),players[x*2][1],int(players[(x*2)+1][0]),players[(x*2)+1][1])
        matches.append(match)
    return matches
