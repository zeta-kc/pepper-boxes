#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
main block for backend modules
"""

from bottle import route, run, template
import printgcal
<<<<<<< HEAD
import gcal
=======
import pushcall

>>>>>>> 55a641ae30381117214664673b74c358caab330d

@route('/hello/<name>')
def index(name):
    """
    Test funtion
    """
    return template('<b>Hello {{name}}</b>!', name=name)


@route('/call')
def call():
    """
    Call to a personnel via voice message or instant messege
    """
    pushcall.notify()
    return ""


@route('/schedule')
def get_schedule():
    """
    Get Boss's schedule from google calendar
    """
    calendar = gcal.fetch_calendar()
    return calendar


@route('/print/schedule')
def print_schedule():
    """
    Print Boss's schedule from specified printer
    """
    printgcal.print_calendar()
    return ""


"""
Start server
"""
run(host='localhost', port=8080)
