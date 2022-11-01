from src.common.print_text import print_text


def gain_access_to_group(group_key, users, service, stdscr=None):
    for user in users:
        user_representation = {
            "email": user,
            "role": "OWNER",
            "type": "USER",
            "delivery_settings": "ALL_MAIL",
        }
        service.members().insert(groupKey=group_key, body=user_representation).execute()
        print_text(f'Access for {user} in group {group_key} has been successfully granted!', stdscr)
