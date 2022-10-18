from src.common.print_text import print_text


def create_google_group(group_name, service, stdsct=None):
    creating_group = f'Creating Google Group with name {group_name}'
    print_text(creating_group, stdsct)

    group = {}
    service.groups().create(body=group).execute()
