import sys

from curses import wrapper

from src.cli.available_options import setup_available_options
from src.cli.cli_actions_navigator import cli_execute

from src.exceptions.index import SingleArgument
from src.common.index import CLI_OPERATIONS


def cli(argv):
    options = setup_available_options(argv)
    operation = []
    set_options = {}

    for i in options.__dict__:
        if options.__dict__[i] is not None and options.__dict__[i]:
            if i in CLI_OPERATIONS:
                operation.append(i)
            else:
                set_options[i] = options.__dict__[i]

    try:
        if len(operation) != 1:
            raise SingleArgument
    except SingleArgument:
        print('One operation argument is expected.')
        sys.exit()
    cli_execute(operation[0], set_options)
    sys.exit()


def interactive_cli(stdscr):
    pass


def main(argv):
    if len(argv) > 0:
        cli(argv)
    else:
        wrapper(interactive_cli)


if __name__ == '__main__':
    main(sys.argv[1:])
