def forward_email(email_from, email_to, service):
    results = service.users().labels().list(userId=email_from).execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
        return
    print('Labels:')
    for label in labels:
        print(label['name'])

    # label_name = 'IMPORTANT'
    # filter_content = {
    #     'criteria': {
    #         'from': email_from
    #     },
    #     'action': {
    #         'addLabelIds': [label_name],
    #         'removeLabelIds': ['INBOX'],
    #         'forward': email_to
    #     }
    # }
    #
    # service.users().settings().filters().create(
    #     userId=email_from, body=filter_content
    # ).execute()
    #
    # print(f'Email forwarding from {email_from} to {email_to} has been enabled!')
