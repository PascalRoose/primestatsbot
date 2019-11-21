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

import os
import pickle
from copy import deepcopy
from enum import Enum

from primestatsbot.primestats import PRIMESTATS

_thisdir = os.path.dirname(os.path.realpath(__file__))

# Load chatsettings from pickle if it exists
try:
    with open(os.path.join(_thisdir, 'resources/chatsettings.pickle'), 'rb') as chatsettings_in:
        chatsettings = pickle.load(chatsettings_in)
# Else create a new empty dictionary
except FileNotFoundError:
    chatsettings = {}


# Enumerate for copymodes
class Copymode(Enum):
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


def save_chatsettings():
    """Save chatsettings as pickle"""
    with open(os.path.join(_thisdir, 'resources/chatsettings.pickle'), 'wb+') as chatsettings_out:
        pickle.dump(chatsettings, chatsettings_out)
