#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ** Stats Converter **
# This is a simple Telegram bot for converting exported stats from Ingress Prime to a nicely formatted message
#
# - Author: PascalRoose
# - Repo: https://github.com/PascalRoose/primestatsbot.git
#

import os
import pickle
from copy import deepcopy
from enum import Enum

from appdirs import user_cache_dir

from primestatsbot.resources.primestats import PRIMESTATS

filename = os.path.join(user_cache_dir("primestatsbot"), "chatsettings.pickle")

# Load chatsettings from pickle if it exists, create new one otherwise
try:
    with open(filename, 'rb') as chatsettings_in:
        chatsettings = pickle.load(chatsettings_in)
except FileNotFoundError:
    chatsettings = {}


class Copymode(Enum):
    """Enumerate for copymodes"""
    NONE = 0
    VALUES_ONLY = 1
    NAME_AND_VALUE = 2
    ALL = 3


def add_chatsettings(tg_id):
    """Add user to chatsettings with default settings"""
    # Make a copy of PRIMESTATS and change all values from 'units' to booleans indicating show/hide
    show_stats = deepcopy(PRIMESTATS)
    for cat, stats in PRIMESTATS.items():
        for stat_name, _ in stats.items():
            # Show all stats by default
            show_stats[cat][stat_name] = True

    # Default chatsettings
    chatsettings[tg_id] = {
        'copy': Copymode.NONE.value,
        'headers': True,
        'stats': show_stats,
        'units': True
    }

    save_chatsettings()


def get_chatsettings(tg_id):
    return deepcopy(chatsettings[tg_id])


def update_chatsettings(tg_id, new_chatsettings):
    chatsettings[tg_id] = new_chatsettings
    save_chatsettings()


def save_chatsettings():
    with open(filename, 'wb+') as chatsettings_out:
        pickle.dump(chatsettings, chatsettings_out)
