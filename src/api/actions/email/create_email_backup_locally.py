import os
import sqlite3
import time
import base64
import datetime
import curses

from src.api.common.call_api import call_api_pages, call_api
from src.api.common.database import message_is_backed_up

from src.common.print_text import print_text
from src.common.functions import rewrite_line

global gmail, local_folder, sqlcur


def create_email_backup(email_from, service, stdscr=None, return_objects=False):
    if stdscr is not None:
        h, w = curses.getsyx()
    else:
        h = None

    global gmail
    gmail = service

    global local_folder
    local_folder = f'gmcli-gmail-backup-{email_from}'

    sql_db_file = os.path.join(local_folder, 'msg-db.sqlite')
    new_db = not os.path.isfile(sql_db_file)

    sqlconn = sqlite3.connect(':memory:')
    sqlconn.execute('''CREATE TABLE settings (name TEXT PRIMARY KEY, value TEXT);''')
    sqlconn.execute('''INSERT INTO settings (name, value) VALUES (?, ?);''',
                    ('email_address', email_from))
    sqlconn.execute('''INSERT INTO settings (name, value) VALUES (?, ?);''',
                    ('db_version', '6'))
    sqlconn.execute('''CREATE TABLE messages(message_num INTEGER PRIMARY KEY,
                             message_filename TEXT,
                             message_internaldate TIMESTAMP);''')
    sqlconn.execute('''CREATE TABLE labels (message_num INTEGER, label TEXT);''')
    sqlconn.execute('''CREATE TABLE uids (message_num INTEGER, uid TEXT PRIMARY KEY);''')
    sqlconn.execute('''CREATE UNIQUE INDEX labelidx ON labels (message_num, label);''')
    sqlconn.commit()

    global sqlcur
    sqlcur = sqlconn.cursor()

    page_message = 'Got %%total_items%% Message IDs'
    messages_to_process = call_api_pages(
        service.users().messages(),
        'list',
        items='messages',
        page_message=page_message,
        maxResults=500,
        userId='me',
        includeSpamTrash=False,
        fields='nextPageToken,messages/id',
        stdscr=stdscr
    )

    backup_path = local_folder
    if not os.path.isdir(backup_path):
        os.mkdir(backup_path)
    messages_to_backup = []
    messages_to_refresh = []

    for message_num in messages_to_process:
        if not new_db and message_is_backed_up(message_num['id'], sqlcur, local_folder):
            messages_to_refresh.append(message_num['id'])
        else:
            messages_to_backup.append(message_num['id'])

    backup_count = len(messages_to_backup)

    backed_up_messages = 0
    gbatch = service.new_batch_http_request()

    for a_message in messages_to_backup:
        call_api(gbatch, None, soft_errors=True)
        gbatch = service.new_batch_http_request()
        sqlconn.commit()
        rewrite_line(f'Backed up {backed_up_messages} of {backup_count} messages.', h, stdscr)

        gbatch.add(service.users().messages().get(
            userId='me',
            id=a_message,
            format='raw',
            fields='id,labelIds,internalDate,raw'
        ), callback=backup_message)
        backed_up_messages += 1

    if len(gbatch._order) > 0:
        call_api(gbatch, None, soft_errors=True)
        sqlconn.commit()
        rewrite_line(f'Backed up {backed_up_messages} of {backup_count} messages.', h, stdscr)
    print("\n")

    messages_to_refresh = []
    refreshed_messages = 0

    sqlcur.executescript("""CREATE TEMP TABLE current_labels (label TEXT);""")

    gbatch = service.new_batch_http_request()
    for a_message in messages_to_refresh:
        gbatch.add(service.users().messages().get(
            userId='me',
            id=a_message,
            format='minimal',
            fields='id,labelIds'
        ), callback=refresh_message)
        refreshed_messages += 1

        if len(gbatch._order) == 0:
            call_api(gbatch, None, soft_errors=True)
            gbatch = service.new_batch_http_request()
            sqlconn.commit()
            rewrite_line(f'Backed up {backed_up_messages} of {backup_count} messages.', h, stdscr)

    if len(gbatch._order) > 0:
        call_api(gbatch, None, soft_errors=True)
        sqlconn.commit()
        rewrite_line(f'Backed up {backed_up_messages} of {backup_count} messages.', h, stdscr)
    print("\n")

    if return_objects:
        return {
            'local_folder': local_folder,
            'sqlcur': sqlcur,
            'sqlconn': sqlconn
        }


def label_ids_to_labels(label_ids):
    all_label_ids = dict()
    global gmail
    labels = list()
    for labelId in label_ids:
        if labelId not in all_label_ids:
            label_results = call_api(gmail.users().labels(), 'list',
                                     userId='me', fields='labels(name,id,type)')
            all_label_ids = dict()
            for a_label in label_results['labels']:
                if a_label['type'] == 'system':
                    all_label_ids[a_label['id']] = a_label['id']
                else:
                    all_label_ids[a_label['id']] = a_label['name']
        try:
            labels.append(all_label_ids[labelId])
        except KeyError:
            pass
    return labels


def backup_message(request_id, response, exception):
    if exception is not None:
        print_text(exception)
    else:
        label_ids = response.get('labelIds', [])

        if 'CHATS' in label_ids or 'CHAT' in label_ids:
            return

        labels = label_ids_to_labels(label_ids)
        message_file_name = "%s.eml" % (response['id'])
        message_time = int(response['internalDate']) / 1000
        message_date = time.gmtime(message_time)

        try:
            time_for_sqlite = datetime.datetime.fromtimestamp(message_time)
        except (OSError, IOError, OverflowError):
            time_for_sqlite = datetime.datetime.fromtimestamp(86400)

        message_rel_path = os.path.join(str(message_date.tm_year),
                                        str(message_date.tm_mon),
                                        str(message_date.tm_mday))

        message_rel_filename = os.path.join(message_rel_path, message_file_name)
        message_full_path = os.path.join(local_folder, message_rel_path)
        message_full_filename = os.path.join(local_folder, message_rel_filename)

        if not os.path.isdir(message_full_path):
            os.makedirs(message_full_path)

        raw_message = str(response['raw'])
        full_message = base64.urlsafe_b64decode(raw_message)

        with open(message_full_filename, 'wb') as f:
            f.write(full_message)

        sqlcur.execute("""
             INSERT INTO messages (
                         message_filename, 
                         message_internaldate) VALUES (?, ?)""",
                       (message_rel_filename,
                        time_for_sqlite))
        message_num = sqlcur.lastrowid

        sqlcur.execute("""
             REPLACE INTO uids (message_num, uid) VALUES (?, ?)""",
                       (message_num, response['id']))

        for label in labels:
            sqlcur.execute("""
           INSERT INTO labels (message_num, label) VALUES (?, ?)""",
                           (message_num, label))


def refresh_message(request_id, response, exception):
    if exception is not None:
        raise exception
    else:
        if 'labelIds' in response:
            labels = label_ids_to_labels(response['labelIds'])
            sqlcur.execute('DELETE FROM current_labels')
            sqlcur.executemany(
                'INSERT INTO current_labels (label) VALUES (?)',
                ((label,) for label in labels))
            sqlcur.execute("""DELETE FROM labels where message_num = 
                   (SELECT message_num from uids where uid = ?)
                    AND label NOT IN current_labels""", ((response['id']),))
            sqlcur.execute("""INSERT INTO labels (message_num, label) 
            SELECT message_num, label from uids, current_labels 
               WHERE uid = ? AND label NOT IN 
               (SELECT label FROM labels 
                  WHERE message_num = uids.message_num)""",
                           ((response['id']),))
