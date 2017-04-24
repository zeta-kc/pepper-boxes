#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
main block for backend modules
"""

from bottle import route, run, template
import printgcal


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
    return ""


@route('/schedule')
def get_schedule():
    """
    Get Boss's schedule from google calendar
    """
    return ""


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
