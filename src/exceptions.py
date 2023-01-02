class ServerAPIError(Exception):
    pass


class UserAlreadyExistsError(ServerAPIError):
    pass


class UserNotFoundError(ServerAPIError):
    pass


class ShopInfoNotFoundError(ServerAPIError):

    def __init__(self, *args, key: str):
        super().__init__(*args)
        self.key = key


class SupportTicketCreationRateLimitExceededError(ServerAPIError):

    def __init__(self, seconds_to_wait: int | float):
        super().__init__()
        self.seconds_to_wait = seconds_to_wait
