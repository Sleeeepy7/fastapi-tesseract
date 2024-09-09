# блок в тесте, пока думаю как централизовать ошибки


class SubscriptionPlanNotFoundError(ValueError):
    pass


class UserNotFoundError(ValueError):
    pass


class InsufficientFundsError(ValueError):
    pass


class ActiveSubscriptionError(ValueError):
    pass
