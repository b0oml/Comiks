from abc import ABC, abstractmethod


class Provider(ABC):

    def __init__(self, config=None):
        self.config = config or {}

    def is_available(self):
        return self.config.get('enabled', True)

    @abstractmethod
    def get_repositories(self, username):
        pass
