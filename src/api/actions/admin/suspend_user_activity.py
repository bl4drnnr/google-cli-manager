def suspend_user(email, service):
    print('Suspending user account...')
    try:
        user = service.users().get(userKey=email).execute()
        user['suspended'] = True
        service.users().update(userKey=email, body=user).execute()
        print('User\'s account activity has been successfully suspended!')
    except Exception as e:
        raise Exception(e)
