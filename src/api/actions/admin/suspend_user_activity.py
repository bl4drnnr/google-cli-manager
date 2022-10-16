from src.common.print_text import print_text


def suspend_user(email, service, stdscr=None):
    suspending_user = f'Suspending {email} account...'
    print_text(suspending_user, stdscr)

    user = service.users().get(userKey=email).execute()
    user['suspended'] = True
    service.users().update(userKey=email, body=user).execute()

    success = f'User\'s account {email} activity has been successfully suspended!'
    print_text(success, stdscr)
