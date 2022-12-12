import curses

from src.interactive_cli.prints import InteractiveCliPrints

from src.common.variables import MENU, AVAILABLE_FUNCTIONS, PAD_HEIGHT
from src.common.functions import pad_refresh


class InteractiveCliExecutor:
    def __init__(self, stdscr):
        self._stdscr = stdscr

    def init_interactive_cli(self):
        current_row_idx = 0
        InteractiveCliPrints.print_menu(self._stdscr, current_row_idx)
        self._navigate_menu(current_row_idx)

    def _navigate_menu(self, current_row_idx):
        while True:
            key = self._stdscr.getch()
            self._stdscr.clear()

            if key == curses.KEY_UP and current_row_idx > 0:
                current_row_idx -= 1
            elif key == curses.KEY_DOWN and current_row_idx < len(MENU) - 1:
                current_row_idx += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                if MENU[current_row_idx] == 'Exit\n':
                    InteractiveCliPrints.print_exit(self._stdscr)
                elif MENU[current_row_idx] == 'Documentation\n':
                    InteractiveCliPrints.print_documentation(self._stdscr)
                else:
                    height, width = self._stdscr.getmaxyx()
                    y = 0
                    pad = curses.newpad(PAD_HEIGHT, width)

                    current_row_idx = 0

                    InteractiveCliPrints.print_functions_menu(pad, y, current_row_idx, height, width)
                    res = self._navigate_functions_menu(pad, y, current_row_idx, height, width)

                    if res == 0:
                        return

            InteractiveCliPrints.print_menu(self._stdscr, current_row_idx)
            self._stdscr.refresh()

    def _navigate_functions_menu(self, pad, pad_pos, current_row_idx, height, width):
        pad.getch()
        while True:
            key = self._stdscr.getch()

            if key == ord('q') or key == ord('Q'):
                return 0

            if key == curses.KEY_UP and current_row_idx > 0:
                current_row_idx -= 1
            elif key == curses.KEY_DOWN and current_row_idx < len(AVAILABLE_FUNCTIONS) - 1:
                current_row_idx += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                selected_command = AVAILABLE_FUNCTIONS[current_row_idx].split('\n')[0]
                InteractiveCliPrints.print_selected_command(self._stdscr, selected_command)

            InteractiveCliPrints.print_functions_menu(pad, pad_pos, current_row_idx, height, width)
            pad_refresh(pad, current_row_idx, height, width)
