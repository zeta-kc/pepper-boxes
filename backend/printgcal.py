#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
print schedule from google calendar
"""

# standard libraries
from datetime import datetime as dt
import socket

# extend libraries
from bottle import template
import pdfkit

# constants
PORT_JETDIRECT = 9100
TEMP_PDF_FILE = 'out.pdf'
PRINTER_HOST = '127.0.0.1'

def create_pdf_file():
    """
    create pdf file function
    """
    schedule = ['10:00-11:00 会議1', '11:00-12:00 会議2']
    now = dt.now().strftime('%Y/%m/%d')
    html = template('schedule', date=now, schedule=schedule)
    options = {
        'page-size': 'A4',
        'margin-top': '0.1in',
        'margin-right': '0.1in',
        'margin-bottom': '0.1in',
        'margin-left': '0.1in',
        'encoding': "UTF-8",
        'no-outline': None
    }
    pdfkit.from_string(html, TEMP_PDF_FILE, options=options)

def print_pdf(host_name, file_name):
    """
    Print pdf file via TCP/IP(JetDirect) function
    """
    with open(file_name, "rb") as pdf_file:
        buf = pdf_file.read()
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host_name, PORT_JETDIRECT))
        client.send(buf)

def print_calendar():
    """
    print schedule from google calendar function
    """
    #Get calendar
    create_pdf_file()
    #print_pdf(PRINTER_HOST, TEMP_PDF_FILE)

if __name__ == "__main__":
    print_calendar()
