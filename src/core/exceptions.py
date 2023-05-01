class ServerAPIError(Exception):
    pass


class NotFoundError(ServerAPIError):
    status_code = 404


class ConflictError(ServerAPIError):
    status_code = 409


class TooManyRequestsError(ServerAPIError):
    status_code = 429


class UserNotFoundError(NotFoundError):
    pass


class NotEnoughProductStocksError(NotFoundError):
    pass


class CartProductNotFoundError(NotFoundError):
    pass


class ProductNotFoundError(NotFoundError):
    pass


class TicketNotFoundError(NotFoundError):
    pass


class UserHasNoTicketsError(NotFoundError):
    pass


class ShopInfoNotFoundError(NotFoundError):

    def __init__(self, *args, key: str):
        super().__init__(*args)
        self.key = key


class CartProductAlreadyExistsError(ConflictError):
    pass


class ClosedTicketError(ConflictError):
    pass


class UserAlreadyExistsError(ConflictError):
    pass


class SupportTicketCreationRateLimitExceededError(TooManyRequestsError):

    def __init__(self, *args, seconds_to_wait: int | float):
        super().__init__(*args)
        self.seconds_to_wait = seconds_to_wait


class SupportTicketsNotFoundError(NotFoundError):
    pass
