from abc import ABC, abstractmethod


class Provider(ABC):

    name = ''
    url = ''
    tags = []

    def __init__(self, config=None):
        self.config = config or {}

    def is_available(self, tags):
        if tags is not None:
            return any([
                tag in self.tags
                for tag in tags
            ])
        return self.config.get('enabled', True)

    @abstractmethod
    def get_user_infos(self, username):
        pass

    @abstractmethod
    def get_repositories(self, user_infos):
        pass
