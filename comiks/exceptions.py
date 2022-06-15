'''Custom exceptions.'''

class AuthException(Exception):
    '''Authentication error (commonly to an API).'''


class NotFoundException(Exception):
    '''The asked resource has not been found.'''
