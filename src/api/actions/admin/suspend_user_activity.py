def suspend_user(email, service):
    print('Suspending user account...')
    try:
        user = service.users().get(userKey=email).execute()
        user['suspended'] = True
        return user
    except Exception as e:
        raise Exception(e)
