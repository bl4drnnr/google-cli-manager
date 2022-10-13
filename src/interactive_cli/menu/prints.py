import sys
import curses

from src.common.index import LOGO, MENU


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


def print_documentation(stdscr):
    pass


def print_exit(stdscr):
    print_logo(stdscr, 3)
    stdscr.addstr('Bye...\n\n')
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
            else:
                stdscr.addstr(f' > {row}', curses.color_pair(1))
        else:
            if row == 'Exit\n':
                stdscr.addstr(row, curses.color_pair(3))
            else:
                stdscr.addstr(row)

    stdscr.refresh()

