class Error(Exception):
    pass


class SingleArgument(Error):
    pass


class WrongOption(Error):
    pass


class WrongAttributes(Error):
    pass


class NoCredentialsFile(Error):
    pass
