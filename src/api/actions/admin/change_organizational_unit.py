from src.common.functions import print_text


def change_organizational_unit(email, service, ou, stdscr=None):
    print_text(f'Changing user OU on {ou}...', stdscr)

    user = service.users().get(userKey=email).execute()
    user['orgUnitPath'] = f'/{ou}'
    service.users().update(userKey=email, body=user).execute()

    print_text('User\'s Organizational Unit has been successfully updated!', stdscr)
