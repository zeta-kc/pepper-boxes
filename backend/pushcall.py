#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
main block for backend modules
"""

import os

from pushbullet import Pushbullet

def notify():
    """
    push call notification.
    """
    pushb = Pushbullet(os.environ.get('PUSHBULLET_KEY', ''))
    push = pushb.push_note("野水さんから", "橋本さん、早く来て！")
    print push
