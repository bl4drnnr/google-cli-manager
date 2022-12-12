from src.common.functions import print_text


def archive_user_account(email, service, stdscr):
    print_text(f'Archiving {email} user account...', stdscr)

    user = service.users().get(userKey=email).execute()
    user['archived'] = True
    service.users().update(userKey=email, body=user).execute()

    print_text(f'User {email} has been successfully archived!', stdscr)
