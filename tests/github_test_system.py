import datetime
import os
import pytest
from github import Github
from app.github_client import GithubClient


GITHUB_ACCESS_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN')

assert GITHUB_ACCESS_TOKEN is not None


@pytest.fixture(scope='module')
def py_github_client():
    yield Github(GITHUB_ACCESS_TOKEN)


@pytest.fixture
def app_github_client():
    yield GithubClient(GITHUB_ACCESS_TOKEN)


def test_get_pull(py_github_client):
    repo = py_github_client.get_repo("PyGithub/PyGithub")
    pr = repo.get_pull(664)
    assert pr.title == "Use 'requests' instead of 'httplib'"
    assert pr.number == 664


def test_github_client(app_github_client):
    timestamp = datetime.datetime(2022, 10, 8)
    numbers = [pr.number for pr in app_github_client.list_pull_requests("PyGithub/PyGithub", timestamp)]
    assert 2324 in numbers

