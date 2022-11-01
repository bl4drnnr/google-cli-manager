def get_group_by_email(group_email, service):
    groups = []
    page_token = None

    while True:
        response = service.groups().list(
            customer='my_customer',
            maxResults=200,
            pageToken=page_token
        ).execute()

        groups.extend(response.get('groups', []))
        page_token = response.get('nextPageToken', None)

        if page_token is None:
            break

    for group in groups:
        if group['email'] == group_email:
            return group
