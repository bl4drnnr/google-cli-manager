class Error(Exception):
    pass


class SingleArgument(Error):
    pass


class NoToken(Error):
    pass


class WrongOption(Error):
    pass


class WrongAttributes(Error):
    pass
