import argparse

from tabulate import tabulate

from comiks.authors import get_authors, taint_authors
from comiks.colors import DIM, GREEN, RST
from comiks.config import load_config
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
    print(f' 🔎 {provider.name} {DIM}({provider.url}){RST}')

    user_infos = provider.get_user_infos(username)
    repos = provider.get_repositories(user_infos)

    for repo in repos:
        print(f'\n 📦 {repo.name}')
        authors = get_authors(repo.url)
        taint_authors(authors, highlight)
        print_authors(authors, score_threshold)


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
        help='Highlight a string in output (default is username).',
        required=False,
    )
    args = parser.parse_args()
    # Load config
    config = load_config(args.config)
    provider_config = config.get('provider', {})
    # Search authors for each provider
    for provider_class in PROVIDERS:
        provider = provider_class(
            provider_config.get(provider_class.name, {})
        )
        if provider.is_available():
            run_provider(
                provider,
                args.username,
                args.highlight or args.username,
                config.get('score_threshold', 0.4)
            )


if __name__ == '__main__':
    main()
