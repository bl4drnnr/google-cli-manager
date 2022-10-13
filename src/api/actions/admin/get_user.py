from src.api.service_initiator import init_services


def get_user(email, file_name):
    try:
        service = init_services(file_name, 'admin', 'directory_v1')
        user = service.users().get(userKey=email).execute()
        return user
    except Exception as e:
        raise Exception(e)