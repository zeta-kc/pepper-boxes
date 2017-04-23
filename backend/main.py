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
    for test funtion
    """
    return template('<b>Hello {{name}}</b>!', name=name)

@route('/call')
def call():
    """
    Call to Mr. Hashimoto via Skype voice message
    """
    return ""

@route('/schedule')
def get_schedule():
    """
    Get Mr. Nomizu's schedule from google calendar
    """
    return ""

@route('/print/schedule')
def print_schedule():
    """
    Print Mr. Nomizu's schedule from specified printer
    """
    return ""

"""
Start server
"""
run(host='localhost', port=8080)
