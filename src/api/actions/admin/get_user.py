import json
import curses

from src.common.variables import PAD_HEIGHT
from src.common.functions import pad_refresh, print_text

user = None


def get_user(email, service, stdscr=None):
    global user
    user = service.users().get(userKey=email).execute()

    if stdscr is None:
        print(json.dumps(user, indent=4))
        return

    height, width = stdscr.getmaxyx()
    y = 0
    current_row_idx = 0
    pad = curses.newpad(PAD_HEIGHT, width)

    print_user(pad, y, height, width)
    res = navigate_user(stdscr, pad, y, current_row_idx, height, width)

    if res == 0:
        return


def print_user(stdscr, pad_pos, height, width):
    stdscr.clear()

    print_text(f'Here is info about {user["primaryEmail"]}', stdscr)
    print_text(json.dumps(user, indent=4), stdscr)
    stdscr.addstr('\n\nPress Q to get back...\n\n')

    pad_refresh(stdscr, pad_pos, height, width)


def navigate_user(stdscr, pad, pad_pos, current_row_idx, height, width):
    while True:
        key = stdscr.getch()

        if key == ord('q') or key == ord('Q'):
            return 0

        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN:
            current_row_idx += 1

        print_user(pad, pad_pos, height, width)
        pad_refresh(pad, current_row_idx, height, width)
