import curses

from src.interactive_cli.menu.prints import \
    print_introduction, \
    print_menu, \
    print_documentation, \
    print_exit

from src.common.index import MENU


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
                pass

        print_menu(stdscr, current_row_idx)
        stdscr.refresh()
