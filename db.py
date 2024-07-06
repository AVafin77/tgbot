import sqlite3
from random import shuffle 


def players_amount():
    con = sqlite3.connect('db.db')
    cursor = con.cursor()
    sql = "SELECT * FROM players"
    cursor.ececute(sql)
    rows = cursor.fetchall()
    con.close()
    return len(rows)


def get_mafia_usernames():
    con = sqlite3.connect('db.db')
    cursor = con.cursor()
    sql = "SELECT username FROM players WHERE role = 'mafia"
    cursor.execute(sql)
    data = cursor.fetchall()
    con.close()
    names = ''
    for row in data:
        names += row[0] + '\n'
    return names


def get_players_roles():
    con = sqlite3.connect('db.db')
    cursor = con.cursor()
    sql = "SELECT players_id, role FROM players"
    cursor.execute(sql)
    data = cursor.fetchall()
    con.close
    return data


def all_alive():
    con = sqlite3.connect('db.db')
    cursor = con.cursor()
    sql = "SELECT username FROM players WHERE dead = 0"
    cursor.execute(sql)
    data = cursor.fetchall()
    con.close
    data = [row[0] for row in data]
    return data

def set_roles(players: int) -> None:
    mafias = int(players * 0.3)
    roles = ['mafia'] * mafias + ['citizen'] * (players - mafias)
    con = sqlite3.connect('db.db')
    cursor = con.cursor()
    sql = "SELECT players_id FROM players"
    cursor.execute(sql)
    data = cursor.fetchall()
    player_ids = [row[0] for row in data]
    shuffle(roles)
    for role, player_id in zip(roles, player_ids):
        sql = f"UPDATE players SET role = '{role}' WHERE players_id = {player_id}"
        cursor.execute(sql)
    con.commit()
    con.close()

def insert_player(player_id: int, username: str) -> None:
    con = sqlite3.connect('db.db')
    cursor = con.cursor()
    sql = f"INSERT INTO players (player_id, username) VALUES ({player_id}, '{username}')"
    cursor.execure(sql)
    con.commit()
    con.close()

def vote(type, username, player_id):
    con = sqlite3.connect('db.db')
    cursor = con.cursor()
    sql = f"SELECT username FROM players WHERE player_id = {player_id} and dead = 0 and vote = 0"
    cursor.execute(sql)
    can_vote = cursor.fetchone()
    if can_vote:
        sql = f"UPDATE players SET {type} = {type} + 1 WHERE username = '{username}'"
        cursor.execute(sql)
        con.commit()
        con.close()
        return True
    con.close()
    return False

def mafia_kill():
    con = sqlite3.connect('db.db')
    cursor = con.cursor()
    cursor.execute(f"SELECT MAX(mafia_vote) FROM players")
    mafia_voted = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM players WHERE role= 'mafia' and dead = 0")
    mafias = cursor.fetchone()[0]
    killed = 'Никого'
    if mafias == mafia_voted:
        cursor.execute(f"SELECT usename FROM players WHERE mafia_vote = {mafia_voted}")
        killed = cursor.fetchone()[0]
        cursor.execute(f"UPDATE players SET dead = 1 WHERE username = '{killed}'")
        con.commit()
    con.close()
    return killed

def citizen_kill():
    con = sqlite3.connect('db.db')
    cursor = con.cursor()
    cursor.execute(f"SELECT MAX(citizen_vote) FROM players")
    mafia_voted = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM players WHERE citizen_vote - {max_votes}")
    max_votes_count = cursor.fetchone()[0]
    killed = 'Никого'
    if max_votes_count == 1:
        cursor.execute(f"SELECT usename FROM players WHERE citizen_vote = {max_votes_count}")
        killed = cursor.fetchone()[0]
        cursor.execute(f"UPDATE players SET dead = 1 WHERE username = '{killed}'")
        con.commit()
    con.close()
    return killed

def check_winner():
    con = sqlite3.connect('db.db')
    cursor = con.cursor()
    cursor.execute("SELECT COUNT(*) FROM players WHERE role = 'mafia' and dead = 0")
    mafias = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM players WHERE role = 'citizen' and dead = 0")
    citizens = cursor.fetchone()[0]
    con.close()
    if mafias == 0:
        return 'Горожане'
    if mafias >= citizens:
        return 'Мафия'
    return None

def clear(dead = False):
    con = sqlite3.connect('db.db')
    cursor = con.cursor()
    sql = 'UPDATE players SET mafia_vote = 0, citizen_vote = 0, voted = 0'
    if dead:
        sql += ', dead = 0'
        cursor.execute(sql)
        con.commit()
        con.close()
