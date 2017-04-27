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
    pushb = Pushbullet("o.ZhbZSPLdUVZ7dUlSBDqVAtzolFxaofG8")
    push = pushb.push_note("野水さんから", "橋本さん、早く来て！")
    print push
