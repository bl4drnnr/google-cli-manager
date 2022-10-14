import os
import sys
import curses

from src.common.vars import LOGO, MENU, AVAILABLE_FUNCTIONS, PAD_HEIGHT, pad_refresh, navigation_control
from src.common.credential_file import generate_credentials_file

from src.interactive_cli.menu.docs import commands_docs
from src.oauth2_service.check_client_id_and_secret import check_client_id_and_secret


def print_raw_input(stdscr, prompt_string):
    curses.echo()
    stdscr.addstr(prompt_string)
    stdscr.refresh()
    user_input = stdscr.getstr()
    return user_input.decode('utf-8')


def print_logo(stdscr, color_pair_id):
    h, w = stdscr.getmaxyx()

    for idx, row in enumerate(LOGO):
        x = w // 2 - len(row) // 2
        stdscr.addstr(idx, x, row, curses.color_pair(color_pair_id))


def print_introduction(stdscr):
    print_logo(stdscr, 2)
    stdscr.addstr('Welcome to Google Merger - application that will allow you to manage\n', curses.A_BOLD)
    stdscr.addstr('your and other users\' account(s) of Google Admin Workspace.\n\n', curses.A_BOLD)

    stdscr.addstr('Right before you start, please, read documentation in order to\n')
    stdscr.addstr('prepare all needed accesses and files with credentials.\n\n')

    stdscr.addstr('If you have any issues with access (you\'ve got an error)\n')
    stdscr.addstr('contact your Google Admin Workspace administrator to obtain proper accesses.\n\n')

    stdscr.addstr('Use ')
    stdscr.addstr('ARROWS', curses.A_BOLD)
    stdscr.addstr(' on your keyboard for navigations.\n')
    stdscr.addstr('Press ')
    stdscr.addstr('ENTER', curses.A_BOLD)
    stdscr.addstr(' to confirm your choice.\n\n')


def print_functions_introduction(stdscr):
    print_logo(stdscr, 2)
    stdscr.addstr('Here is list of available functions.\n\n', curses.A_BOLD)

    stdscr.addstr('Use ')
    stdscr.addstr('ARROWS', curses.A_BOLD)
    stdscr.addstr(' on your keyboard for navigations.\n')
    stdscr.addstr('Press ')
    stdscr.addstr('ENTER', curses.A_BOLD)
    stdscr.addstr(' to confirm your choice.\n\n')

    stdscr.addstr('Press Q to get back to main menu...\n\n', curses.A_BOLD)


def print_documentation(stdscr):
    height, width = stdscr.getmaxyx()
    pad_pos = 0
    pad = curses.newpad(PAD_HEIGHT, width)

    print_logo(pad, 2)
    pad.addstr('All functions and deeper descriptions were already described\n')
    pad.addstr('in ')
    pad.addstr('README', curses.A_BOLD)
    pad.addstr(' file. Below will be listed only short definition for them\n')
    pad.addstr('but, most important, how to work with different types of\n')
    pad.addstr('Google Accounts', curses.A_BOLD)
    pad.addstr(' like ')
    pad.addstr('Service Account', curses.A_BOLD)
    pad.addstr(' and what type of credentials\n')
    pad.addstr('you will need in order to obtain access to different endpoints.\n\n')

    pad.addstr('### DESCRIPTION OF AVAILABLE FUNCTIONS ###\n\n',
               curses.color_pair(2) | curses.A_BOLD | curses.A_UNDERLINE)
    pad.addstr('Because of fact, that Google has a lot of services, there will be\n')
    pad.addstr('described only ones which have been implemented in certain services.\n\n')

    pad.addstr('Gmail\n\n', curses.A_BOLD | curses.A_UNDERLINE)
    pad.addstr('Docs\n\n', curses.A_BOLD | curses.A_UNDERLINE)
    pad.addstr('Drive\n\n', curses.A_BOLD | curses.A_UNDERLINE)
    pad.addstr('Calendar\n\n', curses.A_BOLD | curses.A_UNDERLINE)

    pad.addstr('### CREDENTIALS ###\n\n', curses.color_pair(2) | curses.A_BOLD | curses.A_UNDERLINE)
    pad.addstr('### BACKUPS ###\n\n', curses.color_pair(2) | curses.A_BOLD | curses.A_UNDERLINE)

    pad.addstr('In case of any issues, don\'t hesitate to text me - ')
    pad.addstr('mikhail.bahdashych@protonmail.com\n\n', curses.A_BOLD | curses.A_UNDERLINE)

    pad.addstr('Press Q to get back to main menu...')

    pad_refresh(pad, pad_pos, height, width)
    navigation_control(pad, pad_pos, height, width)


def print_exit(stdscr):
    print_logo(stdscr, 4)
    stdscr.addstr('Hope you had fun. Bye...\n\n', curses.A_BOLD)

    stdscr.addstr('In order to obtain more information about Google API\n')
    stdscr.addstr('or other SDKs see - ')
    stdscr.addstr('https://developers.google.com\n\n', curses.A_UNDERLINE)

    stdscr.addstr('Press any key to exit...')
    stdscr.getch()
    sys.exit()


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


def print_menu(stdscr, current_row_idx):
    stdscr.clear()

    print_introduction(stdscr)
    for idx, row in enumerate(MENU):

        if idx == current_row_idx:
            if row == 'Start\n':
                stdscr.addstr(f' > {row}', curses.color_pair(2))
            elif row == 'Documentation\n':
                stdscr.addstr(f' > {row}', curses.color_pair(4))
            elif row == 'Exit\n':
                stdscr.addstr(f' > {row}', curses.color_pair(3))
        else:
            if row == 'Start\n':
                stdscr.addstr(row, curses.color_pair(2))
            elif row == 'Documentation\n':
                stdscr.addstr(row, curses.color_pair(4))
            elif row == 'Exit\n':
                stdscr.addstr(row, curses.color_pair(3))

    stdscr.refresh()


def print_functions_menu(stdscr, current_row_idx):
    stdscr.clear()

    print_functions_introduction(stdscr)
    for idx, row in enumerate(AVAILABLE_FUNCTIONS):

        if idx == current_row_idx:
            stdscr.addstr(f' > {row}', curses.color_pair(1))
        else:
            stdscr.addstr(row)

    stdscr.refresh()


def print_selected_command(stdscr, command):
    stdscr.clear()

    command_execution(stdscr, command)
