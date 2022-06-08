from comiks.provider.bitbucket import BitbucketProvider
from comiks.provider.github import GithubProvider
from comiks.provider.gitlab import GitlabProvider

PROVIDERS = [
    GithubProvider,
    GitlabProvider,
    BitbucketProvider,
]
