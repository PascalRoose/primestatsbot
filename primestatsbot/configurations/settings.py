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

TOKEN = '599256047:AAE8Z_YqSF_J7OudQYplaJU29mv3wmDSAC0'  # Bot API Token
NAME = 'pascal_testbot'  # Username of the bot (without @)
ADMIN = 129626744  # Telegram ID of the admin user

WEBHOOK = False

# The following configuration is only needed if you setted WEBHOOK to True
WEBHOOK_OPTIONS = {
    'listen': '0.0.0.0',  # IP
    'port': 443,
    'url_path': TOKEN,  # This is recommended for avoiding random people
    #  making fake updates to your bot
}
WEBHOOK_URL = f'https://example.com/{WEBHOOK_OPTIONS["url_path"]}'
