import sqlite3
from enum import Enum

tgBotToken = '1237564925:AAFaS1k8MKAjEo60QrE8rcCxyBYwkRyszLU'
api_key = "427366b5e50ddf04869a914ad94224a2dec7f38c"
output_type = '2'
numres = 5
minsim ='70!'
dbmask = 8589938016

class States(Enum):
    S_START = 0
    S_REQUEST_Media = 1
    #S_REQUEST_tgChannel = 1
    S_REQUEST_vkDomain = 2
    S_REQUEST_vkToken = 3
    S_REQUEST_confirmation = 4

def set_state(user_id, value):
    conn = sqlite3.connect('states.db')
    cursor = conn.cursor()
    sql_select = 'SELECT * FROM states where user_id={}'.format(user_id)
    sql_insert = "INSERT INTO states VALUES ({}, {})".format(user_id, value)
    sql_add_state = 'UPDATE states SET state={} WHERE user_id={}'.format(value, user_id)
    cursor.execute(sql_select)
    data = cursor.fetchone()
    if data is None:
        cursor.execute(sql_insert)
        conn.commit()
    if data is not None:
        cursor.execute(sql_add_state)
        conn.commit()
    conn.close()

def get_current_state(user_id):
    conn = sqlite3.connect('states.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM states where user_id={}'.format(user_id))
    row = cursor.fetchone()
    conn.close()
    return row[1]
