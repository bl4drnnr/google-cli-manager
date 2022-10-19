from src.api.service_initiator import init_group_service
from src.api.actions.groups.create_group import create_google_group

from src.common.print_text import print_text


def create_groups(group_name, delegated_user, customer_id, stdscr=None):
    try:
        service = init_group_service(delegated_user)
        create_google_group(group_name, customer_id, service, stdscr)
    except Exception as e:
        error = f'An error occurred while creating groups: {e}'
        print_text(error, stdscr, error=True)
