class DomainError(Exception):
    pass


class AccessExpiredError(DomainError):
    pass


class AuthenticationError(DomainError):
    pass
