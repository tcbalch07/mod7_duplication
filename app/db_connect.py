import pymysql
from flask import g

def get_db():
    if 'db' not in g or not is_connection_open(g.db):
        g.db = pymysql.connect(
            host='s54ham9zz83czkff.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',
            user='drq4bw3p8o7pko8t',
            password='j7otmowax9wzbw9y',
            database='n982sk1385219hps',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db

def is_connection_open(conn):
    try:
        conn.ping(reconnect=True)
        return True
    except:
        return False

def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None and not db._closed:
        db.close()