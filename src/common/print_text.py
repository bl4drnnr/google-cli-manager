import curses


def print_text(text, stdscr=None, error=False):
    if stdscr is not None:
        if error:
            stdscr.addstr(f'\n{text}', curses.A_BOLD | curses.color_pair(3))
        else:
            stdscr.addstr(f'\n{text}')
    else:
        print(text)
