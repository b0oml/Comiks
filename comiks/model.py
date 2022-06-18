'''Models to represent some entities.'''

# pylint: disable=too-few-public-methods

class UserInfos:
    '''Represents the informations available for an user.'''

    def __init__(self, username, display_name, identifier):
        self.username = username
        self.display_name = display_name
        self.identifier = identifier


class Author:
    '''Represents a commit author/committer.'''

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.branches = []
        self.score = 0

    def __repr__(self):
        return f'{self.name} <{self.email}>'


class Repository:
    '''Represents a Git repository.'''

    def __init__(self, name, url, fork=False):
        self.name = name
        self.url = url
        self.fork = fork
