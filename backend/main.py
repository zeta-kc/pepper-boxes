#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
main block for backend modules
"""

# standard libraries
import os

# extend libraries
from bottle import route, template

# own modules
import printgcal
import gcal
import pushcall

@route('/hello/<name>')
def index(name):
    """
    Test funtion
    """
    print 'main:index - called.'
    return template('<b>Hello {{name}}</b>!', name=name)


@route('/call')
def call():
    """
    Call to a personnel via voice message or instant messege
    """
    print 'main:call - called.'
    pushcall.notify()
    return 'Done'


@route('/schedule')
def get_schedule():
    """
    Get Boss's schedule from google calendar
    """
    print 'main:get_schedule - called.'
    calendar = gcal.fetch_calendar()
    return calendar

@route('/print/schedule')
def print_schedule():
    """
    Print Boss's schedule from specified printer
    """
    print 'main:print_schedule - called.'
    printgcal.print_calendar()
    return 'Done'

if __name__ == "__main__":
    """
    Start server
    """
    import bottle
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())
    bottle.TEMPLATE_PATH.insert(0, './backend/views/')
    bottle.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
