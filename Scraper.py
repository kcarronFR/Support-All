#! /usr/bin/env python3
import os.path
from github import Github
from github import Auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1bMZLrLc7Nxw1u7da2L-QaFvPokZuOvOGFG4QgYLsFwo"
SAMPLE_RANGE_NAME = "Import Data!A2:E"


auth = Auth.Token("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")
creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
        token.write(creds.to_json())


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
                        print(trimmed_import)
                        importArray.append(trimmed_import)
                        try:
                            service = build("sheets", "v4", credentials=creds)

                            # Call the Sheets API
                            sheet = service.spreadsheets()
                            result = (
                            sheet.values()
                            .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
                            .execute()
                            )
                            values = result.get("values", [])

                            if not values:
                                print("No data found.")
                                return

                            print("Name, Another Name:")
                            for row in values:
                            # Print columns A and E, which correspond to indices 0 and 4.
                                print(f"{row[0]}, {row[4]}")
                        except HttpError as err:
                            print(err)
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