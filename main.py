import sys
import curses

from curses import wrapper

from src.interactive_cli.menu_navigator import InteractiveCliExecutor
from src.cli.cli_actions_navigator import CliExecutor

from src.exceptions.index import SingleArgument
from src.common.variables import CLI_OPERATIONS


def cli(argv):
    options = CliExecutor.setup_available_options(argv)
    operation = []
    set_options = {}

    for i in options.__dict__:
        if options.__dict__[i] is not None and options.__dict__[i]:
            if i in CLI_OPERATIONS:
                operation.append(i)
            else:
                set_options[i] = options.__dict__[i]

    try:
        if len(operation) != 1 and set_options != {'delete': True}:
            raise SingleArgument
        if set_options == {'delete': True}:
            operation = ['']
    except SingleArgument:
        print('One operation argument is expected.')
        sys.exit()

    cli_executor = CliExecutor(operation[0], set_options)
    cli_executor.cli_execute()

    sys.exit()


def interactive_cli(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)

    interactive_cli_executor = InteractiveCliExecutor(stdscr)
    interactive_cli_executor.init_interactive_cli()


def main(argv):
    if len(argv) > 0:
        cli(argv)
    else:
        wrapper(interactive_cli)


if __name__ == '__main__':
    main(sys.argv[1:])
