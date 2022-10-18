from src.common.print_text import print_text
from src.api.actions.groups.create_group import create_google_group

from src.api.service_initiator import init_services


def create_groups(group_name, stdscr=None):
    try:
        service = init_services('groupsmigration', 'v1')
        create_google_group(group_name, service, stdscr)
    except Exception as e:
        error = f'An error occurred while creating groups: {e}'
        print_text(error, stdscr, error=True)
