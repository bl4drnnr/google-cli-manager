from src.common.print_text import print_text


def merge_calendar(email_from, email_to, service, stdscr=None):
    rule = {
        'scope': {
            'type': 'user',
            'value': email_to,
        },
        'role': 'owner'
    }
    service.acl().insert(calendarId=email_from, body=rule).execute()

    success = 'All events have been transferred successfully.'
    print_text(success, stdscr)
