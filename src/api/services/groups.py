from src.api.service_initiator import init_group_service, ServiceInitiator

from src.api.actions.groups.create_group import create_google_group
from src.api.actions.groups.get_group_by_email import get_group_by_email
from src.api.actions.groups.gain_access_to_group import gain_access_to_group

from src.common.functions import print_text


def create_groups(group_name, delegated_user, customer_id, stdscr=None):
    try:
        service = init_group_service(delegated_user)
        create_google_group(group_name, customer_id, service, stdscr)
    except Exception as e:
        error = f'An error occurred while creating groups: {e}'
        print_text(error, stdscr, error=True)


def gain_group_access(group_key, users, stdscr=None):
    try:
        service_initiator = ServiceInitiator('admin')
        service = service_initiator.init_services()
        group = get_group_by_email(group_key, service)
        gain_access_to_group(group['id'], users, service, stdscr)
    except Exception as e:
        error = f'An error occurred while patching access to the group: {e}'
        print_text(error, stdscr, error=True)
