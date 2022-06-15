'''Comiks Provider module entrypoint.'''

from comiks.provider.bitbucket import BitbucketProvider
from comiks.provider.github import GithubProvider
from comiks.provider.gitlab import GitlabProvider

# List of all available providers
PROVIDERS = [
    GithubProvider,
    GitlabProvider,
    BitbucketProvider,
]
