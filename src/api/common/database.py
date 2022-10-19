import os
import sys
import sqlite3


def message_is_backed_up(message_num, sqlcur, backup_folder):
    try:
        sqlcur.execute('''
         SELECT message_filename FROM uids NATURAL JOIN messages
                where uid = ?''', (message_num,))
    except sqlite3.OperationalError as e:
        if e.message == 'no such table: messages':
            print("\n\nError: your backup database file appears to be corrupted.")
        else:
            print("SQL error:%s" % e)
        sys.exit(8)
    sql_req = sqlcur.fetchall()
    for x in sql_req:
        filename = x[0]
        if os.path.isfile(os.path.join(backup_folder, filename)):
            return True
    return False
