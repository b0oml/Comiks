
import tempfile

import git
import requests
from fastDamerauLevenshtein import damerauLevenshtein

from comiks.model import Author


def get_authors(repo_url):
    authors = set()
    temp_dir = tempfile.TemporaryDirectory()

    repo = git.Repo.clone_from(repo_url, temp_dir.name)

    for ref in repo.heads:
        for commit in repo.iter_commits(ref.name):
            authors.add(
                Author(commit.author.name, commit.author.email)
            )
            authors.add(
                Author(commit.committer.name, commit.committer.email)
            )

    temp_dir.cleanup()

    return authors


def taint_authors(authors, token):
    lower_token = token.lower()
    for author in authors:
        score_name = damerauLevenshtein(author.name.lower(), lower_token)
        score_email = damerauLevenshtein(author.email.split('@')[0].lower(), lower_token)
        author.score = max(score_name, score_email)
