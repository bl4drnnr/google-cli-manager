def merge_calendar(email_from, email_to, service):
    rule = {
        'scope': {
            'type': 'user',
            'value': email_to,
        },
        'role': 'owner'
    }
    service.acl().insert(calendarId=email_from, body=rule).execute()
    print('All events have been transferred successfully.')
