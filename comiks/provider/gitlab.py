'''GitLab provider.'''

import requests

from comiks.exceptions import AuthException, NotFoundException
from comiks.model import UserInfos, Repository
from comiks.provider.base import Provider


class GitlabProvider(Provider):
    '''Get user infos and repositories from GitLab provider.'''

    name = 'GitLab'
    url = 'gitlab.com'
    tags = ['gitlab']

    def __get(self, endpoint, params=None, paginated=False):
        results = []
        params = params or {}

        if paginated:
            params['per_page'] = 100

        page = 1
        while True:
            if paginated:
                params['page'] = page

            resp = requests.get(
                f'https://gitlab.com/api/v4{endpoint}',
                params=params,
                headers={
                    'PRIVATE-TOKEN': self.config['access_token'],
                }
            )
            if resp.status_code == 401:
                raise AuthException()

            data = resp.json()

            if not paginated or not isinstance(data, list):
                results = data
                break

            results.extend(data)

            if len(data) < 100:
                break

            page += 1

        return results

    def get_user_infos(self, username):
        resp = self.__get('/users', {'username': username})

        if len(resp) == 0:
            raise NotFoundException()

        return UserInfos(
            username=resp[0]['username'],
            display_name=resp[0]['name'],
            identifier=resp[0]['id'],
        )

    def get_repositories(self, user_infos):
        # Get events with action created
        events = self.__get(f'/users/{user_infos.identifier}/events?action=created', paginated=True)
        project_ids = [event['project_id'] for event in events]
        # Get events with action joined
        events = self.__get(f'/users/{user_infos.identifier}/events?action=joined', paginated=True)
        project_ids.extend([event['project_id'] for event in events])
        # Get name and URL for each project
        for project_id in project_ids:
            project = self.__get(f'/projects/{project_id}')
            # Check that we have repository access
            if project['repository_access_level'] != 'enabled':
                continue
            yield Repository(
                name=project['name_with_namespace'],
                url=project['http_url_to_repo'],
                fork=project.get('forked_from_project', False),
            )
