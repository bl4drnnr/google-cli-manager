import os
import googleapiclient
import hashlib

from io import BytesIO

from src.api.common import fmbox
from src.api.common.call_api import call_api
from src.common.print_text import print_text
from src.common.functions import rewrite_line

mbox_extensions = ['mbx', 'mbox', 'eml']
suffixes = ['b', 'kb', 'mb', 'gb', 'tb', 'pb']


def percentage(part, whole):
    return '{0:.2f}'.format(100 * float(part) / float(whole))


def humansize(myobject):
    if isinstance(myobject, (str, bytes)):
        n_bytes = os.stat(myobject).st_size
    else:
        n_bytes = myobject
    if n_bytes == 0:
        return '0 B'
    i = 0
    while n_bytes >= 1024 and i < len(suffixes) - 1:
        n_bytes /= 1024.
        i += 1
    f = ('%.2f' % n_bytes).rstrip('0').rstrip('.')
    return '%s%s' % (f, suffixes[i])


def restore_msg_to_group(gmig, full_message, message_num, sqlconn, group_id, stdscr=None):
    fstr = BytesIO(full_message)
    media = googleapiclient.http.MediaIoBaseUpload(fstr, mimetype='message/rfc822', chunksize=-1, resumable=True)
    try:
        call_api(gmig.archive(), 'insert', groupId=group_id, media_body=media, soft_errors=True)
    except googleapiclient.errors.MediaUploadSizeError:
        error_message = 'ERROR: Message is to large for groups. Skipping...'
        print_text(error_message, stdscr, error=True)
        return
    sqlconn.execute('INSERT OR IGNORE INTO restored_messages (message_num) VALUES (?)', (message_num,))
    sqlconn.commit()


def restore_group(email_from, service, local_folder, sqlcur, sqlconn, stdscr=None):
    max_message_size = service._rootDesc['resources']['archive']['methods']['insert']['mediaUpload']['maxSize']
    print_text(f'Groups supports restore of messages up to {max_message_size}', stdscr)
    resume_db = os.path.join(local_folder, "%s-restored.sqlite" % email_from)

    gyb_format = os.path.isfile(os.path.join(local_folder, 'msg-db.sqlite'))
    if gyb_format:
        sqlcur.execute('ATTACH ? as resume', (resume_db,))

        sqlcur.executescript('''CREATE TABLE IF NOT EXISgTS resume.restored_messages (message_num INTEGER PRIMARY KEY); 
        CREATE TEMP TABLE skip_messages (message_num INTEGER PRIMARY KEY);''')

        sqlcur.execute('''INSERT INTO skip_messages SELECT message_num
                    FROM restored_messages''')

        sqlcur.execute('''SELECT message_num, message_internaldate,
                    message_filename FROM messages WHERE message_num NOT IN skip_messages ORDER BY message_internaldate DESC''')

        messages_to_restore_results = sqlcur.fetchall()
        restore_count = len(messages_to_restore_results)
        current = 0
        for x in messages_to_restore_results:
            current += 1
            rewrite_line(f'Restoring message {current} of {restore_count} from {x[1]}', stdscr)

            message_num = x[0]
            message_filename = x[2]

            if not os.path.isfile(os.path.join(local_folder, message_filename)):
                print_text(f'WARNING! File {os.path.join(local_folder, message_filename)} does not exist for message {message_num}.', stdscr)
                print_text('This message will be skipped.', stdscr)
                continue
            with open(os.path.join(local_folder, message_filename), 'rb') as f:
                full_message = f.read()
            group_id = email_from.split('@')[0] + 'backup' + email_from.split('@')[1]
            restore_msg_to_group(service, full_message, message_num, sqlconn, group_id)
    else:
        sqlcur.execute('ATTACH ? as resume', (resume_db,))
        sqlcur.executescript('''CREATE TABLE IF NOT EXISTS resume.restored_messages (message_num TEXT PRIMARY KEY)''')
        sqlcur.execute('SELECT message_num FROM resume.restored_messages')

        messages_to_skip_results = sqlcur.fetchall()
        messages_to_skip = []

        for a_message in messages_to_skip_results:
            messages_to_skip.append(a_message[0])

        for path, sub_dirs, files in os.walk(local_folder):
            for filename in files:
                file_extension = filename.split('.')[-1]
                if file_extension not in mbox_extensions:
                    continue
                file_path = os.path.join(path, filename)
                print_text(f'Restoring from {humansize(file_path)} file {file_path}.')
                mbox = fmbox.fmbox(file_path)
                current = 0
                while True:
                    current += 1
                    message_marker = '%s-%s' % (file_path, current)
                    request_id = hashlib.md5(message_marker.encode('utf-8')).hexdigest()[:25]
                    if request_id in messages_to_skip:
                        rewrite_line(f'Skipping already restored message #{current}', stdscr)

                        try:
                            mbox.skip()
                        except StopIteration:
                            break
                        continue

                    try:
                        message = mbox.next()
                    except StopIteration:
                        break

                    mbox_pct = percentage(mbox._mbox_position, mbox._mbox_size)
                    rewrite_line(f'Message {current} - {mbox_pct}%', stdscr)
                    full_message = message.as_bytes()
                    group_id = email_from.split('@')[0] + 'backup' + email_from.split('@')[1]
                    restore_msg_to_group(service, full_message, request_id, sqlconn, group_id=group_id)

    sqlconn.commit()
    sqlconn.execute('DETACH resume')
    sqlconn.commit()
