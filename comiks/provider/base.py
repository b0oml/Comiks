from abc import ABC, abstractmethod


class Provider(ABC):

    def __init__(self, config=None):
        pass

    def is_available(self):
        return True

    @abstractmethod
    def get_repositories(self, username):
        pass
