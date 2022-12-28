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


class ShopInfoNotFoundError(ServerAPIError):

    def __init__(self, *args, key: str):
        super().__init__(*args)
        self.key = key
