#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ** Stats Converter **
# This is a simple Telegram bot for converting exported stats from Ingress Prime to a nicely formatted message
#
# - Author: PascalRoose
# - Repo: https://github.com/PascalRoose/primestatsbot.git
#

import datetime
import os
import pickle

from appdirs import user_cache_dir

filename = os.path.join(user_cache_dir("primestatsbot"), "history.pickle")

# Load usersettings from pickle if it exists
try:
    with open(filename, 'rb') as history_in:
        history = pickle.load(history_in)
# Else create a new empty dictionary
except FileNotFoundError:
    history = {}


def add_record(tg_id: int):
    """Add a record to the usage history"""

    # Get todays date
    today = datetime.datetime.now().strftime('%d-%m-%Y')

    # Add todays date to history if it's not in there yet
    if today not in history:
        history[today] = {}
    # Add user to todays history if it's not in there yet
    if tg_id not in history[today]:
        history[today][tg_id] = 0

    # Add one usage to user for today
    history[today][tg_id] += 1

    # Save after every change
    with open(filename, 'wb+') as history_out:
        pickle.dump(history, history_out)


def get_usage_total():
    """Get the total amount of usages"""
    usage = 0
    for day, dayhistory in history.items():
        for user, usages in history[day].items():
            usage += usages

    return usage


def get_usage_week():
    """Get the amount of usages for last week"""

    # Get todays date
    today = datetime.datetime.now()

    # Get all dates from last week (today till today - 6 days)
    days = []
    for i in range(7):
        day = today - datetime.timedelta(days=i)
        days.append(day.strftime('%d-%m-%Y'))

    usage = 0
    for day in days:
        if day in history:
            for user, usages in history[day].items():
                usage += usages

    return usage


def get_users_total():
    """Get the total amount of unique users"""
    users = []

    for day, dayhistory in history.items():
        for user, usages in history[day].items():
            users.append(user)

    # Turn list into set (only unique users), return the length of the list
    return len(set(users))


def get_users_week():
    """Get the number of unique users this week"""

    # Get todays date
    today = datetime.datetime.now()

    # Get all dates from last week (today till today - 6 days)
    days = []
    for i in range(7):
        day = today - datetime.timedelta(days=i)
        days.append(day.strftime('%d-%m-%Y'))

    users = []
    for day in days:
        if day in history:
            for user, usages in history[day].items():
                users.append(user)

    # Turn list into set (only unique users), return the length of the list
    return len(set(users))
