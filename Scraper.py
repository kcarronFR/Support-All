#! /usr/bin/env python3

from github import Github
from github import Auth

auth = Auth.Token("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")

g = Github(auth=auth)

importArray = []

repo = g.get_repo("kcarronFR/distanceCalculator")
contents = repo.get_contents("")


def print_contents(repo, content):
    if content.type == 'dir':

        sub_contents = repo.get_contents(content.path)

        for item in sub_contents:

            content = repo.get_contents(item.path)

            if isinstance(content, list):
                continue
            elif content.path.endswith('.jar'):
                continue
            elif content.path.endswith('.java'):
                string_contents = str(content.decoded_content.decode())
                for line in string_contents.splitlines():
                    if line.startswith("import"):
                        str_line = str(line)
                        remove_import = str_line.removeprefix('import')
                        trimmed_import = remove_import.removesuffix(';')

                        importArray.append(trimmed_import)

        if sub_contents:
            print_contents(repo, sub_contents[0])


for repo in g.get_user().get_repos():
    if repo.name == 'distanceCalculator':
        contents = repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == 'dir':
                repo_contents = repo.get_contents(file_content.path)
                popped_contents = repo_contents.pop(0)

                print_contents(repo, popped_contents)

    else:
        continue