import sys
import curses

from src.common.index import LOGO, MENU, AVAILABLE_FUNCTIONS


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

    stdscr.addstr('Press Q to get back to main menu.\n\n', curses.A_BOLD)


def print_documentation(stdscr):
    print_logo(stdscr, 2)
    stdscr.addstr('All functions and deeper descriptions were already described\n')
    stdscr.addstr('in ')
    stdscr.addstr('README', curses.A_BOLD)
    stdscr.addstr(' file. Below will be listed only short definition for them\n')
    stdscr.addstr('but, most important, how to work with different types of\n')
    stdscr.addstr('Google Accounts', curses.A_BOLD)
    stdscr.addstr(' like ')
    stdscr.addstr('Service Account', curses.A_BOLD)
    stdscr.addstr(' and what type of credentials\n')
    stdscr.addstr('you will need in order to obtain access to different endpoints.\n\n')

    stdscr.addstr('### DESCRIPTION OF AVAILABLE FUNCTIONS ###\n\n', curses.color_pair(2) | curses.A_BOLD | curses.A_UNDERLINE)
    stdscr.addstr('### CREDENTIALS ###\n\n', curses.color_pair(2) | curses.A_BOLD | curses.A_UNDERLINE)

    stdscr.addstr('In case of any issues, don\'t hesitate to text me - ')
    stdscr.addstr('mikhail.bahdashych@protonmail.com\n\n', curses.A_BOLD | curses.A_UNDERLINE)

    stdscr.addstr('Press any key to continue...')
    stdscr.getch()


def print_exit(stdscr):
    print_logo(stdscr, 4)
    stdscr.addstr('Hope you had fun. Bye...\n\n', curses.A_BOLD)

    stdscr.addstr('In order to obtain more information about Google API\n')
    stdscr.addstr('or other SDKs see - ')
    stdscr.addstr('https://developers.google.com\n\n', curses.A_UNDERLINE)

    stdscr.addstr('Press any key to exit...')
    stdscr.getch()
    sys.exit()


def print_menu(stdscr, current_row_idx):
    stdscr.clear()

    print_introduction(stdscr)
    for idx, row in enumerate(MENU):

        if idx == current_row_idx:
            if row == 'Exit\n':
                stdscr.addstr(f' > {row}', curses.color_pair(3))
            elif row == 'Start\n':
                stdscr.addstr(f' > {row}', curses.color_pair(2))
            else:
                stdscr.addstr(f' > {row}')
        else:
            if row == 'Exit\n':
                stdscr.addstr(row, curses.color_pair(3))
            elif row == 'Start\n':
                stdscr.addstr(row, curses.color_pair(2))
            else:
                stdscr.addstr(row)

    stdscr.refresh()


def print_functions_menu(stdscr, current_row_idx):
    stdscr.clear()

    print_functions_introduction(stdscr)
    for idx, row in enumerate(AVAILABLE_FUNCTIONS):

        if idx == current_row_idx:
            stdscr.addstr(f' > {row}')
        else:
            stdscr.addstr(row)

    stdscr.refresh()
