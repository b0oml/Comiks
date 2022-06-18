'''Methods relatives to commits authors.'''

import tempfile

import git
from fastDamerauLevenshtein import damerauLevenshtein  # pylint: disable=no-name-in-module

from comiks.model import Author


def __add_author(authors, name, email, branch):
    if (name, email) not in authors:
        authors[(name, email)] = Author(name, email)

    if branch not in authors[(name, email)].branches:
        authors[(name, email)].branches.append(branch)


def get_authors(repo_url):
    '''Get authors/commiters from each commits of a given repository.'''
    authors = {}

    with tempfile.TemporaryDirectory() as temp_dir:
        repo = git.Repo.clone_from(repo_url, temp_dir)
        for ref in repo.remote().refs:
            if ref.remote_head == 'HEAD':
                continue
            for commit in repo.iter_commits(ref.name):
                __add_author(authors, commit.author.name, commit.author.email, ref.remote_head)
                __add_author(authors, commit.committer.name, commit.committer.email, ref.remote_head)

    return authors.values()


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
