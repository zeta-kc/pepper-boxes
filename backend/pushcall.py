#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
main block for backend modules
"""

from pushbullet import Pushbullet


def notify():
    """
    push call notification.
    """
    pushb = Pushbullet("o.9GpEBJ3D7pQzR5nAmEm3Fq5ywX3f2S50")
    push = pushb.push_note("This is the title", "This is the body")
    print push
