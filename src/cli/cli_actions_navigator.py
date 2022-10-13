import sys

from src.exceptions.index import WrongOption

from src.api.services.email import enable_email_forwarding
from src.api.services.drive import transfer_drive_ownership
from src.api.services.calendar import transfer_calendar_events
from src.api.services.admin import suspend_user_activity

FILE_NAME = 'credentials.json'


def cli_execute(operation, options):
    off_board_user = options['email_from']
    user_to_transfer = options['email_to']

    try:
        if operation == 'offboard':
            suspend_user_activity(off_board_user, FILE_NAME)
            transfer_calendar_events(off_board_user, user_to_transfer, FILE_NAME)
            transfer_drive_ownership(off_board_user, user_to_transfer, FILE_NAME)
            enable_email_forwarding(off_board_user, user_to_transfer, FILE_NAME)
        elif operation == 'sua':
            suspend_user_activity(off_board_user, FILE_NAME)
        elif operation == 'tce':
            transfer_calendar_events(off_board_user, user_to_transfer, FILE_NAME)
        elif operation == 'tdo':
            transfer_drive_ownership(off_board_user, user_to_transfer, FILE_NAME)
        elif operation == 'ef':
            enable_email_forwarding(off_board_user, user_to_transfer, FILE_NAME)
        else:
            raise WrongOption
    except WrongOption:
        print('Wrong option.')
        sys.exit()
