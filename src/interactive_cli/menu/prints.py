import sys
import curses

from src.common.variables import MENU, AVAILABLE_FUNCTIONS, PAD_HEIGHT
from src.common.functions import pad_refresh, navigation_control, print_logo
from src.interactive_cli.menu.menu_actions import command_execution


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

    pad.addstr('### CREDENTIALS ###\n\n', curses.color_pair(2) | curses.A_BOLD | curses.A_UNDERLINE)
    pad.addstr('Every action requires user to have proper access.\n')
    pad.addstr('In every case, in order to obtain access to functions, you will\n')
    pad.addstr('need to provide ')
    pad.addstr('OAuth 2.0 credentials.\n\n', curses.A_BOLD)

    pad.addstr('Some of operation are available only in Google Admin Workspace (G Suite).\n')
    pad.addstr('In order to have access to these operation you need to have proper accesses as user.\n')
    pad.addstr('If you want to get access to other users\' data (what you probably want to do)\n')
    pad.addstr('you need to have ')
    pad.addstr('Service Account.\n', curses.A_BOLD)
    pad.addstr('This type of account allows you to get access to other users\' data\n')
    pad.addstr('by escalating privileges from you to this account.\n\n')
    pad.addstr('If you got any access error, please, ')
    pad.addstr('contact your Google Admin Workspace administrator.\n\n', curses.A_BOLD)

    pad.addstr('### DESCRIPTION OF AVAILABLE FUNCTIONS ###\n\n',
               curses.color_pair(2) | curses.A_BOLD | curses.A_UNDERLINE)
    pad.addstr('Because of fact, that Google has a lot of services, there will be\n')
    pad.addstr('described only ones which have been implemented in certain services.\n\n')

    pad.addstr('General\n\n', curses.A_BOLD | curses.A_UNDERLINE)
    pad.addstr('Offboard user ', curses.A_BOLD)
    pad.addstr('- common offboarding procedure that includes a couple of operations.\n')
    pad.addstr('Operation that is triggered while offboarding procedure:\n')
    pad.addstr('1. Suspend user activity.\n')
    pad.addstr('2. Changes user Organizational Unit.\n')
    pad.addstr('3. Transfer GDrive ownership.\n')
    pad.addstr('4. Transfer Google Calendar events ownership.\n')
    pad.addstr('5. Backup of user\'s email by creating Google Group.\n\n')

    pad.addstr('Suspend user activity ', curses.A_BOLD)
    pad.addstr('- changes user\'s account status to "suspended", \nbut doesn\'t archive it.\n\n')

    pad.addstr('Change user Organizational Unit ', curses.A_BOLD)
    pad.addstr('- changes user\'s Organizational Unit (OU). \nOU should already exists in Workspace.\n\n')

    pad.addstr('Drive\n\n', curses.A_BOLD | curses.A_UNDERLINE)
    pad.addstr('Transfer GDrive ownership ', curses.A_BOLD)
    pad.addstr('- transfers ownership of files on Google Drive, that\nhas been created by this user.\n\n')

    pad.addstr('Calendar\n\n', curses.A_BOLD | curses.A_UNDERLINE)
    pad.addstr('Transfer Google Calendar events ', curses.A_BOLD)
    pad.addstr('- transfers all user\'s Google Calendar events\nto another calendar. ')
    pad.addstr('Receiver of events receives email with\nproposition to add those events ')
    pad.addstr('to his private Google Calendar.\n\n')

    pad.addstr('Docs\n\n', curses.A_BOLD | curses.A_UNDERLINE)
    pad.addstr('Transfer Google Docs ownership ', curses.A_BOLD)
    pad.addstr('- transfers ownership of files on Google Docs, that\nhas been created by this user.\n\n')

    pad.addstr('Gmail\n\n', curses.A_BOLD | curses.A_UNDERLINE)
    pad.addstr('Local email back up ', curses.A_BOLD)
    pad.addstr('- creates backup of user\'s emails and saves it locally.\n\n')

    pad.addstr('Google Groups email back up ', curses.A_BOLD)
    pad.addstr('- creates backup of user\'s emails\nand uploads it in form of Google Group.\n\n')

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
