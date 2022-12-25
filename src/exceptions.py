class ServerAPIError(Exception):
    pass


class UserAlreadyExistsError(ServerAPIError):
    pass


class UserNotFoundError(ServerAPIError):
    pass


class SupportSubjectAlreadyExistsError(ServerAPIError):
    pass


class SupportSubjectNotFoundError(ServerAPIError):
    pass
