import curses

from src.api.service_initiator import init_services

from src.api.actions.drive.transfer_ownership import transfer_ownership


def transfer_drive_ownership(email_from, email_to, stdscr=None):
    try:
        service = init_services('drive', 'v3')
        transfer_ownership(email_from, email_to, service)
    except Exception as e:
        error = f'An error occurred while transferring drive ownership: {e}'
        if stdscr is not None:
            stdscr.addstr(f'\n{error}', curses.A_BOLD | curses.color_pair(3))
        else:
            print(error)
