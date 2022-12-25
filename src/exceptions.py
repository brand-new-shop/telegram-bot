class ServerAPIError(Exception):
    pass


class UserAlreadyExistsError(ServerAPIError):
    pass


class UserNotFoundError(ServerAPIError):
    pass
