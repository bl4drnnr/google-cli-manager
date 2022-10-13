from src.api.service_initiator import init_services

from src.api.actions.calendar.merge_calendar import merge_calendar


def transfer_calendar_events(email_from, email_to, file_name):
    try:
        service = init_services(file_name, 'calendar', 'v3', email_from)
        merge_calendar(email_from, email_to, service)
    except Exception as e:
        print(f'An error occurred: {e}')
