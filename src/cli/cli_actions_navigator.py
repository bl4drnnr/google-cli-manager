import os
import sys

from src.exceptions.index import WrongOption, NoCredentialsFile

from src.api.services.email import email_backup
from src.api.services.drive import transfer_drive_ownership
from src.api.services.calendar import transfer_calendar_events
from src.api.services.admin import suspend_user_activity
from src.api.services.admin import change_ou


def cli_execute(operation, options):
    try:
        off_board_user = options['email_from']
        user_to_transfer = options['email_to']

        if not os.path.exists('credentials.json'):
            raise NoCredentialsFile

        try:
            if operation == 'offboard':
                suspend_user_activity(off_board_user)
                transfer_calendar_events(off_board_user, user_to_transfer)
                transfer_drive_ownership(off_board_user, user_to_transfer)
                email_backup(off_board_user, user_to_transfer)
                change_ou(off_board_user, '')
            elif operation == 'sua':
                suspend_user_activity(off_board_user)
            elif operation == 'tce':
                transfer_calendar_events(off_board_user, user_to_transfer)
            elif operation == 'tdo':
                transfer_drive_ownership(off_board_user, user_to_transfer)
            elif operation == 'cebl':
                email_backup(off_board_user, user_to_transfer)
            elif operation == 'cebg':
                email_backup(off_board_user, user_to_transfer)
            elif operation == 'tgdo':
                pass
            else:
                raise WrongOption
        except WrongOption:
            print('Wrong option!')
            sys.exit()
    except NoCredentialsFile:
        print('No credentials were set!')
        print('Please, check manual with documentation ("-h" or "--help") in order to set them.')
        sys.exit()
