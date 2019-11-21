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


class IncorrectMessageError(Exception):
    """Gets raised when a primestats message was expected but the message wasn't one"""


class AdminDidNotStartBotError(Exception):
    """
    Gets raised if the admin didn't send /start to the bot before running.
    This way the bot can't send the admin any messages over telegram
    """


class InvalidAdminError(Exception):
    """Gets raised when the telegram ID in ADMIN (configurations/settings.py) is invalid"""
