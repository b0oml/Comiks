'''Parent each other provider class should extends.'''

from abc import ABC, abstractmethod


class Provider(ABC):
    '''Provider abstract class.

    Each inherithed class should be able to determine if an user exists or not,
    eventually get informations about this user. And list public repositories
    of the user.
    '''

    name = ''
    url = ''
    tags = []

    def __init__(self, config=None):
        self.config = config or {}

    def is_available(self, tags):
        '''Is the provider available/enabled?.'''
        if tags is not None:
            return any(
                tag in self.tags
                for tag in tags
            )
        return self.config.get('enabled', False)

    @abstractmethod
    def get_user_infos(self, username):
        '''Try to get user informations for the given username.'''

    @abstractmethod
    def get_repositories(self, user_infos):
        '''Get user repositories.'''
