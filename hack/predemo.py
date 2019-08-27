# -*- coding: utf-8 -*-
import datetime
import os
from github import Github
import webbrowser
import requests

USERS = ["nuclearpinguin", "potiuk", "mik-laj", "TobKed"]
DEMO_KEY = os.environ.get("DEMO_KEY", None)


def resolve_pr(commit):
    commit_sha = commit.sha
    headers = {
        "Authorization": f"token {DEMO_KEY}",
        "Accept": "application/vnd.github.groot-preview+json",
    }
    response = requests.get(
        f"https://api.github.com/repos/apache/airflow/commits/{commit_sha}/pulls",
        headers=headers,
    )
    if response.status_code == 200:
        return response.json()[0]["html_url"]
    return commit.html_url


def make_link(commit):
    title = commit.commit.message.split("\n")[0]
    html_url = resolve_pr(commit)
    return "<li><a href={html_url}>{title}</a></li>".format(
        html_url=html_url, title=title
    )


def generate_html_file(commits):
    content = [make_link(c) for c in commits]
    content = ["<ul>"] + content + ["</ul>"]
    print("Saving to file")
    with open("pre-demo.html", "w+") as file:
        file.writelines(content)
    webbrowser.open("file://" + os.path.realpath("pre-demo.html"))


def include(pr, point_in_time):
    if pr.user.login not in USERS:
        return False
    return pr.closed_at > point_in_time


def unique_commit(commits):
    unique_commits_msgs = set()
    unique_commits = []
    for commit in commits:
        if commit.commit.message in unique_commits_msgs:
            continue
        unique_commits_msgs.add(commit.commit.message)
        unique_commits.append(commit)
    return unique_commits


def get_pr_for_demo():
    print("Getting PR for pre-demo [last 6 days]")
    print("This may tak a while")
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=6)
    point_in_time = now - delta
    if not DEMO_KEY:
        raise ValueError("Set DEMO_KEY env variable for Github API")

    g = Github(DEMO_KEY)
    repo = g.get_repo("apache/airflow")
    commits = sum(
        (list(repo.get_commits(author=user, since=point_in_time)) for user in USERS), []
    )
    commits = unique_commit(commits)
    generate_html_file(commits)


if __name__ == "__main__":
    get_pr_for_demo()
