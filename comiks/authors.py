'''Methods relatives to commits authors.'''

import tempfile

import git
from fastDamerauLevenshtein import damerauLevenshtein  # pylint: disable=no-name-in-module

from comiks.model import Author


def get_authors(repo_url):
    '''Get authors/commiters from each commits of a given repository.'''
    authors = set()

    with tempfile.TemporaryDirectory() as temp_dir:
        repo = git.Repo.clone_from(repo_url, temp_dir)
        for ref in repo.remote().refs:
            for commit in repo.iter_commits(ref.name):
                authors.add(
                    Author(commit.author.name, commit.author.email)
                )
                authors.add(
                    Author(commit.committer.name, commit.committer.email)
                )

    return authors


def taint_authors(authors, token):
    '''Give a score to each author, with the goal to highlight some authors.

    For each author, it calculates the distance between name/email and the
    token (a string) given in parameter.
    '''
    lower_token = token.lower()
    for author in authors:
        score_name = damerauLevenshtein(author.name.lower(), lower_token)
        score_email = damerauLevenshtein(author.email.split('@')[0].lower(), lower_token)
        author.score = max(author.score, max(score_name, score_email))
