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

import json
import os

_thisdir = os.path.dirname(os.path.realpath(__file__))

# Load primestats from primestats.json
with open(os.path.join(_thisdir, 'resources/primestats.json'), 'rb') as primestats_json:
    PRIMESTATS = json.load(primestats_json)
