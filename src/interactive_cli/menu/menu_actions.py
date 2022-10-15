import os
import curses

from src.common.credential_file import generate_credentials_file
from src.common.functions import print_raw_input, print_logo

from src.interactive_cli.menu.docs import commands_docs
from src.oauth2_service.check_client_id_and_secret import check_client_id_and_secret


def command_execution(stdscr, command):
    print_logo(stdscr, 4)

    command_instructions = commands_docs[command]

    for idx, row in enumerate(command_instructions):
        if idx == 0:
            stdscr.addstr(f' - {row}', curses.A_BOLD)
        else:
            stdscr.addstr(row)

    if not os.path.exists('credentials.json'):
        client_id = print_raw_input(stdscr, 'Please, provide client ID: ')
        client_secret = print_raw_input(stdscr, 'Please, provide client secret: ')
        project_id = print_raw_input(stdscr, 'Please, provide project ID: ')

        valid_credentials_error = check_client_id_and_secret(client_id, client_secret)

        if len(valid_credentials_error) != 0:
            stdscr.addstr(valid_credentials_error, curses.color_pair(3))
            stdscr.addstr('\n\nPress any key to get back...')
            stdscr.getch()
            return

        generate_credentials_file(client_id, client_secret, project_id)
