import curses


def print_error(error, stdscr=None):
    if stdscr is not None:
        stdscr.addstr(f'\n{error}', curses.A_BOLD | curses.color_pair(3))
    else:
        print(error)
