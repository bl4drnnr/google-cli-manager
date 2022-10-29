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
    stdscr.addstr('###################################\n\n', curses.A_BOLD)


def print_documentation(stdscr):
    height, width = stdscr.getmaxyx()
    pad_pos = 0
    pad = curses.newpad(PAD_HEIGHT, width)

    print_logo(pad, 2)
    pad.addstr('All functions and deeper descriptions were already described ')
    pad.addstr('in ')
    pad.addstr('README', curses.A_BOLD)
    pad.addstr(' file. Below will be listed only short definition for them ')
    pad.addstr('but, most important, how to work with different types of ')
    pad.addstr('Google Accounts', curses.A_BOLD)
    pad.addstr(' like ')
    pad.addstr('Service Account', curses.A_BOLD)
    pad.addstr(' and what type of credentials ')
    pad.addstr('you will need in order to obtain access to different endpoints.\n\n')

    pad.addstr('### CREDENTIALS ###\n\n', curses.color_pair(2) | curses.A_BOLD | curses.A_UNDERLINE)
    pad.addstr('Almost every action requires user to have proper access. ')
    pad.addstr('In every case, in order to obtain access to functions, you will ')
    pad.addstr('need to provide ')
    pad.addstr('OAuth 2.0 credentials.\n\n', curses.A_BOLD)

    pad.addstr('Some of operation are available only in ')
    pad.addstr('Google Admin Workspace (G Suite). ', curses.A_BOLD)
    pad.addstr('In order to have access to these operation you need to have proper accesses as user. ')
    pad.addstr('If you want to get access to other users\' data (what you probably want to do) ')
    pad.addstr('you need to have ')
    pad.addstr('Service Account. ', curses.A_BOLD)
    pad.addstr('This type of account allows you to get access to other users\' data ')
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
    pad.addstr('3. Transfer Google Drive ownership.\n')
    pad.addstr('4. Transfer Google Calendar events ownership.\n')
    pad.addstr('5. Backup of user\'s email by creating Google Group.\n\n')

    pad.addstr('Initiate credentials files ', curses.A_BOLD)
    pad.addstr('- operation used with purpose of generation of regeneration credential files. ')
    pad.addstr('Generates 2 files - personal OAuth 2.0 access file and for Service Account. ')
    pad.addstr('Creates Service Account, if it doesn\'t exist, otherwise, file service.json')
    pad.addstr('in the root of project, can be replaces to your own.\n\n')

    pad.addstr('Suspend user activity ', curses.A_BOLD)
    pad.addstr('- changes user\'s account status to "suspended", but doesn\'t archive it. ')
    pad.addstr('Therefore, there is always ability to activate account.\n\n')

    pad.addstr('Change user Organizational Unit ', curses.A_BOLD)
    pad.addstr('- changes user\'s Organizational Unit (OU). OU should already exists in Workspace.')
    pad.addstr('Used as a part offboarding procedure, but can be used as single operation.\n\n')

    pad.addstr('Get user by email ', curses.A_BOLD)
    pad.addstr('- allows to get information in JSON format about user with provided email. ')
    pad.addstr('Option is available only for users with delegated credentials.\n\n')

    pad.addstr('Drive\n\n', curses.A_BOLD | curses.A_UNDERLINE)
    pad.addstr('Transfer Google Drive ownership ', curses.A_BOLD)
    pad.addstr('- transfers ownership of files on Google Drive, that has been created by this user. ')
    pad.addstr('Other words, transfers ownership of files, that has "owner" permission.\n\n')

    pad.addstr('Calendar\n\n', curses.A_BOLD | curses.A_UNDERLINE)
    pad.addstr('Transfer Google Calendar events ', curses.A_BOLD)
    pad.addstr('- transfers all user\'s Google Calendar events to another calendar. ')
    pad.addstr('Receiver of events receives email with proposition to add those events ')
    pad.addstr('to his private Google Calendar.\n\n')

    pad.addstr('Docs\n\n', curses.A_BOLD | curses.A_UNDERLINE)
    pad.addstr('Transfer Google Docs ownership ', curses.A_BOLD)
    pad.addstr('- transfers ownership of files on Google Docs, that has been created by this user. ')
    pad.addstr('The same situation as for Drive, transfers ownership of files, that has "owner" permission.\n\n')

    pad.addstr('Gmail\n\n', curses.A_BOLD | curses.A_UNDERLINE)
    pad.addstr('Create email backup (locally) ', curses.A_BOLD)
    pad.addstr('- creates backup of user\'s emails and saves it locally. ')
    pad.addstr('Backup is saved as SQLite database, and mostly used in order to restore user\'s email ')
    pad.addstr('and upload backup as Google Group.\n\n')

    pad.addstr('Create email backup (upload to Google Groups) ', curses.A_BOLD)
    pad.addstr('- creates backup of user\'s emails and uploads it in form of Google Group. ')
    pad.addstr('Basically combines 2 operation - creating Google Group and uploading local backup.\n\n')

    pad.addstr('Groups\n\n', curses.A_BOLD | curses.A_UNDERLINE)
    pad.addstr('Create Google Group ', curses.A_BOLD)
    pad.addstr('- creates Google Group. As input data waits for name, ')
    pad.addstr('delegated used email, and customer ID. Used in order to back up emails using Google Group, ')
    pad.addstr('but can be used as single operation.\n\n')

    pad.addstr('------------------------------------------\n\n', curses.A_BOLD)
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


def print_functions_menu(stdscr, pad_pos, current_row_idx, height, width):
    stdscr.clear()

    print_functions_introduction(stdscr)
    for idx, row in enumerate(AVAILABLE_FUNCTIONS):
        if idx == current_row_idx:
            stdscr.addstr(f' > {row}', curses.color_pair(1))
        else:
            stdscr.addstr(row)

    pad_refresh(stdscr, pad_pos, height, width)


def print_selected_command(stdscr, command):
    stdscr.clear()

    command_execution(stdscr, command)
