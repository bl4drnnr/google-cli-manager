def change_organizational_unit(email, service, ou):
    print(f'Changing user OU on {ou}...')
    try:
        user = service.users().get(userKey=email).execute()
        user['orgUnitPath'] = f'/{ou}'
        service.users().update(userKey=email, body=user).execute()
        print('User\'s Google account activity has been successfully suspended!')
    except Exception as e:
        raise Exception(e)
