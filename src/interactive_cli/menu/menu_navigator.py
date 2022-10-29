import curses

from src.interactive_cli.menu.prints import \
    print_menu, \
    print_functions_menu, \
    print_documentation, \
    print_exit, \
    print_selected_command

from src.common.variables import MENU, AVAILABLE_FUNCTIONS, PAD_HEIGHT
from src.common.functions import pad_refresh


def init_interactive_cli(stdscr):
    current_row_idx = 0
    menu_navigator(stdscr, current_row_idx)


def menu_navigator(stdscr, current_row_idx):
    print_menu(stdscr, current_row_idx)
    navigate_menu(stdscr, current_row_idx)


def navigate_menu(stdscr, current_row_idx):
    while True:
        key = stdscr.getch()
        stdscr.clear()

        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(MENU) - 1:
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if MENU[current_row_idx] == 'Exit\n':
                print_exit(stdscr)
            elif MENU[current_row_idx] == 'Documentation\n':
                print_documentation(stdscr)
            else:
                init_start(stdscr)

        print_menu(stdscr, current_row_idx)
        stdscr.refresh()


def init_start(stdscr):
    height, width = stdscr.getmaxyx()
    y = 0
    pad = curses.newpad(PAD_HEIGHT, width)

    current_row_idx = 0

    print_functions_menu(pad, y, current_row_idx, height, width)
    res = navigate_functions_menu(stdscr, pad, y, current_row_idx, height, width)

    if res == 0:
        return


def navigate_functions_menu(stdscr, pad, pad_pos, current_row_idx, height, width):
    pad.getch()
    while True:
        key = stdscr.getch()

        if key == ord('q') or key == ord('Q'):
            return 0

        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(AVAILABLE_FUNCTIONS) - 1:
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            selected_command = AVAILABLE_FUNCTIONS[current_row_idx].split('\n')[0]
            print_selected_command(stdscr, selected_command)

        print_functions_menu(pad, pad_pos, current_row_idx, height, width)
        pad_refresh(pad, current_row_idx, height, width)
