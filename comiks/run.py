import argparse

from tabulate import tabulate

from comiks.authors import get_authors, taint_authors
from comiks.colors import DIM, GREEN, RED, RST
from comiks.config import load_config
from comiks.exceptions import AuthException, NotFoundException
from comiks.provider import PROVIDERS


def print_authors(authors, score_threshold):
    table = []

    for author in authors:
        if author.score >= score_threshold:
            table.append(
                (
                    GREEN + author.name + RST,
                    GREEN + author.email + RST,
                )
            )
        else:
            table.append(
                (
                    author.name,
                    author.email,
                )
            )

    print(tabulate(table, (f'{DIM}Name{RST}', f'{DIM}Email{RST}'), tablefmt='fancy_grid'))


def run_provider(provider, username, highlight, score_threshold):
    print(f'\n 🔎 {provider.name} {DIM}({provider.url}){RST}')

    try:
        user_infos = provider.get_user_infos(username)
    except AuthException:
        print(f'{RED} ⚡ Authentication error, please check your config{RST}')
        return
    except NotFoundException:
        print(f'{RED} ⚡ User not found on {provider.name}{RST}')
        return

    repos = provider.get_repositories(user_infos)
    num_repos = 0

    for repo in repos:
        num_repos += 1
        print(f'\n 📦 {repo.name}')
        authors = get_authors(repo.url)
        for token in highlight.split(','):
            taint_authors(authors, token)
        print_authors(authors, score_threshold)

    if num_repos == 0:
        print(f'{RED} ⚡ No repository found on {provider.name}{RST}')


def main():
    parser = argparse.ArgumentParser(
        description='Retrieve authors informations from commits.'
    )
    parser.add_argument(
        'username',
        help='Username for which to scan commits.'
    )
    parser.add_argument(
        '-c',
        '--config',
        help='Custom config file (default is ~/.config/comiks/config.toml).',
        required=False,
    )
    parser.add_argument(
        '-l',
        '--highlight',
        help='Strings to highlight in output, separated by a comma (default is username).',
        required=False,
    )
    parser.add_argument(
        '-p',
        '--providers',
        dest='tags',
        help='Comma-sperated list of tags to select which providers to enable (default is in config).',
        required=False,
    )
    args = parser.parse_args()
    tags = args.tags.split(',') if args.tags else None
    # Load config
    config = load_config(args.config)
    provider_config = config.get('provider', {})
    # Search authors for each provider
    for provider_class in PROVIDERS:
        provider = provider_class(
            provider_config.get(provider_class.name, {})
        )
        if provider.is_available(tags):
            run_provider(
                provider,
                args.username,
                args.highlight or args.username,
                config.get('score_threshold', 0.4)
            )
    print()


if __name__ == '__main__':
    main()
