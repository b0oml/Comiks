import argparse

from tabulate import tabulate

from comiks.authors import get_authors, taint_authors
from comiks.colors import DIM, GREEN, RST
from comiks.provider import PROVIDERS

SCORE_THRESOLD = 0.4


def print_authors(authors):
    table = []

    for author in authors:
        if author.score >= SCORE_THRESOLD:
            table.append((
                GREEN + author.name + RST,
                GREEN + author.email + RST,
            ))
        else:
            table.append((
                author.name,
                author.email,
            ))

    print(tabulate(table, (f'{DIM}Name{RST}', f'{DIM}Email{RST}'), tablefmt='fancy_grid'))


def run_provider(provider, username):
    print(f' 🔎 Github {DIM}(github.com){RST}')

    repos = provider.get_repositories(username)

    for repo in repos:
        print(f'\n 📦 {repo.name}')
        authors = get_authors(repo.url)
        taint_authors(authors, username)
        print_authors(authors)


def main():
    parser = argparse.ArgumentParser(description='Retrieve authors informations from commits.')
    parser.add_argument('username', help='Username for which to scan commits.')
    args = parser.parse_args()
    for provider_class in PROVIDERS:
        provider = provider_class()
        if provider.is_available():
            run_provider(provider, args.username)


if __name__ == '__main__':
    main()
