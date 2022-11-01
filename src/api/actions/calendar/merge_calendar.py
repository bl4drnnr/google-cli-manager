from src.common.print_text import print_text


def transfer_events(email_from, email_to, service, stdscr=None):
    events = []
    page_token = None

    while True:
        response = service.events().list(
            calendarId=email_from,
            maxResults=200,
            pageToken=page_token
        ).execute()

        events.extend(response.get('items', []))
        page_token = response.get('nextPageToken', None)

        if page_token is None:
            break

    for event in events:
        service.events().move(
            calendarId=email_from,
            eventId=event['id'],
            destination=email_to
        ).execute()

    print_text(f'All events from {email_from} to {email_to} has been transferred successfully', stdscr)
