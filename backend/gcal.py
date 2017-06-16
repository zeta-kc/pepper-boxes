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

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    credentials = client.Credentials.new_from_json(os.environ.get('CALENDAR_TOKEN', ''))
    return credentials

def fetch_calendar():
    """
    Shows basic usage of the Google Calendar API.
    Creates a Google Calendar API service object and outputs a list of one
     day events on the user's calendar.
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
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())
    print(fetch_calendar())
