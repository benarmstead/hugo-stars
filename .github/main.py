import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
from github import Github

URL = "https://themes.gohugo.io/"
g = Github(os.getenv("GITHUB_TOKEN"))


def main():
    resp = requests.get(URL).text
    doc = BeautifulSoup(resp, "html.parser")
    themes = doc.select(
        "body > main > div > div > div.w-100.w-80-l.ph0 > div > section > a")
    f = open("README.md", "w")
    now = datetime.now()
    title = f"# hugo_stars\nUpdated at {now}\Inspired by [hugo_stars](https://github.com/lon9/hugo_stars)\n\n"
    f.write(title)
    f.write("|Name|Stars|Forks|Tags|UpdatedAt|\n----|----|----|----|----\n")

    repos = []
    for theme in themes:
        url = theme["href"]
        print(url)
        resp = requests.get(url).text
        page = BeautifulSoup(resp, "html.parser")
        git_url = page.select(
            "body > main > article > div.flex-l.bg-light-gray > div:nth-child(1) > div:nth-child(2) > div > a:nth-child(1)")
        git_link = ""
        for link in git_url:
            git_link = link["href"]
        tags_selector = page.select(
            "body > main > article > div.flex-l.bg-light-gray > div:nth-child(1) > div:nth-child(1) > ul > li.mb2.mt4 > a")
        tags = []
        for tag_elem in tags_selector:
            tag = tag_elem.get_text().strip()
            if tag:
                tags.append(tag)

        repo = g.get_repo(git_link.replace("https://github.com/", ""))
        repo.tags = tags
        repos.append(repo)

    repos.sort(key=lambda x: x.stargazers_count, reverse=True)

    for repo in repos:
        row = f'|[{repo.name}]({repo.url})|{repo.stargazers_count}|{repo.forks_count}|{", ".join(repo.tags)}|{repo.updated_at}|\n'
        f.write(row)


main()
