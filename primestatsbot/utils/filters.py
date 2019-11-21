#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- style: pep-8 -*-
#
# ** Stats Converter **
# This is a simple Telegram bot for converting exported stats from Ingress Prime to a nicely formatted message
#
# - Author: PascalRoose
# - Repo: https://github.com/PascalRoose/primestatsbot.git
#

from telegram.ext import BaseFilter

from primestatsbot.primestats import PRIMESTATS


class StatsFilter(BaseFilter):
    """Custom filter to check if a primestats message was sent"""

    def filter(self, message):
        # Check if the message contains at least stats in the General category
        return str(message.text).startswith(' '.join(PRIMESTATS['General'].keys()))
