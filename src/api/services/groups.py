from src.common.print_text import print_text


def create_groups(group_name, stdscr=None):
    try:
        pass
    except Exception as e:
        error = f'An error occurred while creating groups: {e}'
        print_text(error, stdscr, error=True)
