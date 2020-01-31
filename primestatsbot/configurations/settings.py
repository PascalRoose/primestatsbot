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

from configparser import ConfigParser
from appdirs import user_config_dir

filename = os.path.join(user_config_dir("primestatsbot"), 'config.ini')

config = ConfigParser()
config.read(filename)

TOKEN = str(config['DEFAULT']['Token'])         # Bot API Token
NAME = str(config['DEFAULT']['Name'])           # Username of the bot (without @)
ADMIN = int(config['DEFAULT']['Admin'])         # Telegram ID of the admin user

if config['Webhook']['Enabled'] == 'true':
    WEBHOOK = True
else:
    WEBHOOK = False

# The following configuration is only needed if you setted WEBHOOK to True
WEBHOOK_OPTIONS = {
    'listen':   str(config['Webhook']['IP']),
    'port':     int(config['Webhook']['Port']),
    'url_path': str(config['Webhook']['Path']),
}
WEBHOOK_URL = str(config['Webhook']['URL'])
