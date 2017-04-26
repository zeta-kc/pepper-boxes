#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
fetch schedule from google calendar
"""
from __future__ import print_function

from datetime import datetime
import json
import os

import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def fetch_calendar():
    """
    Shows basic usage of the Google Calendar API.
    Creates a Google Calendar API service object and outputs a list of one day events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.utcnow()
    end_time = now.replace(hour=14).replace(minute=59).replace(second=59).replace(microsecond=0) #timezone -9
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now.isoformat() + 'Z', timeMax=end_time.isoformat() + 'Z', singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    datas = []
    for event in events:
        data = {
           "start": event['start']['dateTime'],
           "end": event['end']['dateTime'],
           "summary": event['summary']
        }
        datas.append(data)
    return json.dumps({"events": datas})

if __name__ == '__main__':
    fetch_calendar()
