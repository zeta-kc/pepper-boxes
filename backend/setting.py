# coding: utf-8
# 環境変数のあれこれ

import os
import json
import webbrowser

from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
# ================================================================
# 環境変数
# ================================================================

# 表示
# def show_environ():
# for k, v in os.environ.items():
# print("{key} : {value}".format(key=k, value=v))
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_environ(key):
    return os.environ.get(key)


def add_environ(value):
    # 環境変数を追加
    tokens = os.environ['CALENDAR_TOKEN']
    # json.dumps(tokens, ensure_ascii=False)
    dic = json.loads(tokens)
    dic['token_response']['access_token'] = value.access_token

    # tokens = value.access_token
    os.environ['CALENDAR_TOKEN'] = json.dumps(dic)
    for k, v in os.environ.items():
        print("{key} : {value}".format(key=k, value=v))


def get_credentials(code):
    flow = flow_from_clientsecrets('client_secrets.json',
                                   scope='https://www.googleapis.com/auth/calendar',
                                   redirect_uri='http://localhost:5000/settingcallback')
    credentials = flow.step2_exchange(code)
    print credentials.access_token
    return credentials


if __name__ == "__main__":
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())
