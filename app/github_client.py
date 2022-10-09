import datetime
from dataclasses import dataclass, asdict
from io import BytesIO
from typing import Optional, Iterator

from github import Github
import jsonlines


@dataclass
class PullRequestParams:
    """
    Required Parameters for PyGithub
    see: https://docs.github.com/en/rest/pulls/pulls#list-pull-requests
    """
    state: str = 'all'
    sort: str = 'updated'
    direction: str = 'desc'
    base: str = 'master'


class GithubClient:
    """
    Github Client Class.
    Attribute:
        client: PyGithub client instance.
    """
    def __init__(self, access_token: str):
        self.client = Github(access_token)

    def list_pull_requests(self,
                           repository: str,
                           timestamp: datetime.datetime,
                           interval: int = 30,
                           params: Optional[PullRequestParams] = None) -> Iterator:
        """
        Provided a repository, Listing all pull requests by its updated time during
            {timestamp - interval} <  updated_time <= {timestamp}
        """
        repo = self.client.get_repo(repository)
        if params is None:
            params = PullRequestParams()
        for pr in repo.get_pulls(**asdict(params)):
            if timestamp - datetime.timedelta(interval) < pr.updated_at <= timestamp:
                yield pr
            else:
                return

    def fetch(self, 
              repository: str, 
              timestamp: datetime.datetime) -> BytesIO:
        """
        Parsing output from function `list_pull_requests` to JSONL Format as a binary object.
        """
        fp = BytesIO()
        with jsonlines.Writer(fp) as writer:
            for pr in self.list_pull_requests(repository, timestamp):
                writer.write(pr.raw_data)
            return fp
