from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class AnonymousThrottle(AnonRateThrottle):
    """
    Throttle for anonymous (unauthenticated) requests.
    """
    scope = 'anon'
    rate = '20/hour'


class UserThrottle(UserRateThrottle):
    """
    Throttle for authenticated user requests.
    """
    scope = 'user'
    rate = '100/hour'
