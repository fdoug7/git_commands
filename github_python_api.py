import json
import requests
from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()

TOKEN = os.getenv('TOKEN')
REPO_OWNER = os.getenv('OWNER')
REPO_NAME = os.getenv('REPO')


def commit_git_issue(type, priority, description, issue_title):


    if type == 'Bug':
        title = 'Bug | ' + issue_title
    
    if type =='Request':
        title = 'Feature Request | ' + issue_title
    
    body = priority + ' | ' +description

    url = 'https://api.github.com/repos/%s/%s/import/issues' % (REPO_OWNER, REPO_NAME)
    headers = {
        "Authorization": "token %s" % (TOKEN),
        "Accept": "application/vnd.github.golden-comet-preview.json"
    }

    data = {'issue': {'title': title, 'body': body}}

    payload = json.dumps(data)
    response = requests.request("POST", url, data=payload, headers=headers)

    if response.status_code in (200, 202):
        print('[+] Successfully created issue {0:s}'.format(title))
    else:
        print('[-] Could not created issue {0:s}'.format(title))
        print(response)
    

def list_git_issues():
    
    url = 'https://api.github.com/search/issues?q=repo:%s/%s+is:issue&per_page=100' % (REPO_OWNER, REPO_NAME)
    print('url')
    headers = {
        "Authorization": 'token %s' % (TOKEN),
        "Accept": "application/vnd.github.golden-comet-preview.json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        issue = response.json()["items"]
    else:
        issue = [url, response.status_code]

    for i in issue:
        if i['state'] == 'open':
            print('Title: %s; State: %s; ID %i;' % (i['title'], i['state'], i['number']))


def close_git_issue(id):
    print(id)
    url = 'https://api.github.com/repos/%s/%s/issues/%s' % (REPO_OWNER, REPO_NAME, id)
    print(url)
    headers = {
        "Authorization": 'token %s' % (TOKEN),
        "Accept": "application/vnd.github.golden-comet-preview.json"
    }
    data = {
        "state": "close"
    }
    response = requests.patch(url, data=json.dumps(data), headers=headers)
    if response.status_code in (200, 202):
        print("%s closed" % (id))
    else:
        print(response.status_code)


# commit_git_issue('Bug', 'test', 'test', 'Feat')

list_git_issues()