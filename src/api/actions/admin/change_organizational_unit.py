def change_organizational_unit(email, user, service):
    print('Changing user OU on X-Knowde...')
    try:
        user['orgUnitPath'] = '/X-Knowde'
        service.users().update(userKey=email, body=user).execute()
        print('User\'s Google account activity has been successfully suspended!')
    except Exception as e:
        raise Exception(e)
