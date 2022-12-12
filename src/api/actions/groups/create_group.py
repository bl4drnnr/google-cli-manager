from src.common.functions import print_text


def create_google_group(group_name, customer_id, service, stdscr=None):
    print_text(f'Creating group with name: {group_name}', stdscr)

    group_key = {"id": group_name}
    group = {
        "parent": "customers/" + str(customer_id),
        "description": f'Back up group {group_name}',
        "displayName": group_name,
        "groupKey": group_key,
        "labels": {
            "cloudidentity.googleapis.com/groups.discussion_forum": ""
        }
    }

    request = service.groups().create(body=group)
    request.uri += "&initialGroupConfig=WITH_INITIAL_OWNER"
    request.execute()

    print_text(f'Group {group_name} has been successfully created.', stdscr)
