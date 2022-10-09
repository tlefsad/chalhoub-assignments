import datetime
import os
import functions_framework
from app.github_client import GithubClient
from app.bigquery_client import BigQueryClient


GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GCP_TABLE_ID = os.getenv("GCP_TABLE_ID")


@functions_framework.http
def fetch_pull_requests(request):
    """
    Google Cloud Function Entrypoint.
    Fetching all pull requests from the given `repositories` in the request body separated by comma (',')
    Example:
        gcloud functions call $(FUNCTION_NAME) --gen2 --data '{"repositories": "PyGithub/PyGithub,apache/airflow"}'
    """
    request_json = request.get_json(silent=True)

    if request_json and 'repositories' in request_json:
        repositories = request_json['repositories'].split(',')
    else:
        raise ValueError

    bigquery_client = BigQueryClient(GCP_PROJECT_ID)
    github_client = GithubClient(GITHUB_ACCESS_TOKEN)

    timestamp = datetime.datetime.now()
    for repo in repositories:
        payload = github_client.fetch(repo, timestamp)
        bigquery_client.load(GCP_TABLE_ID, payload)
    return f"{timestamp}: Successful Loading pull requests from {repositories}"


