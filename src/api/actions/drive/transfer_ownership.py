def transfer_ownership(email_from, email_to, service):
    print(f'Transferring Google Drive ownership from {email_from} to {email_to}...')
    files = []
    page_token = None
    while True:
        response = service.files().list(spaces='drive',
                                        fields='nextPageToken, '
                                               'files(id, name)',
                                        q=f'"{email_from}" in owners',
                                        pageToken=page_token).execute()

        files.extend(response.get('files', []))
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break

    for file in files:
        perm_owner_id = ''

        file_permission = service.permissions().list(fileId=file['id']).execute()

        for file_perm in file_permission.get('permissions'):
            if file_perm['role'] == 'owner':
                perm_owner_id = file_perm['id']

        file['perm_id'] = perm_owner_id

    for file in files:
        param_perm = {
            'role': 'owner',
            'type': 'user',
            'emailAddress': email_to,
        }

        service.permissions().create(
            fileId=file['id'],
            body=param_perm,
            transferOwnership=True
        ).execute()

        print(f'Access to {file["name"]} has been successfully transferred.')

    print('Access to all files has been transferred successfully!')
