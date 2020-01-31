#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ** Stats Converter **
# This is a simple Telegram bot for converting exported stats from Ingress Prime to a nicely formatted message
#
# - Author: PascalRoose
# - Repo: https://github.com/PascalRoose/primestatsbot.git
#

START_MESSAGE = 'This bot can convert exported stats from Ingress Prime to a nicely formatted message.\n\n' \
                'I can be used in private chat or in a group if you add me.\n\n' \
                'You can Change the format of the output message typing /settings\n\n' \
                'If you dont\'t trust me with your stats you can set up your own bot using' \
                ' [this repository](https://github.com/PascalRoose/primestatsbot)'

HELP_MESSAGE = 'Simply open your agent profile in Ingress Prime and click the copy button in the top right' \
               ' (right under your current Level). Send it to me and I will return a nicely formatted message.\n\n' \
               'If you want to change the look of the output message type /settings'

JOIN_MESSAGE = 'If you grant me administrative rights I can detect messages that are copied from the' \
               ' Ingress Prime scanner and convert them to a nicely formatted message.\n\n' \
               'If you want to change the look of the output message type /settings.' \
               ' Only chat admins can do this.\n\n' \
               'If you dont\'t trust me with your messages or stats you can set up your own bot using' \
               ' [this repository](https://github.com/PascalRoose/primestatsbot)'

INCORRECT_MESSAGE = 'Message format not recognized. Make sure not to alter the copied text.' \
                    ' Just paste it in and send it to me.\n' \
                    'Type /help for instructions'

SETTINGS_MESSAGE = 'Use the buttons below this message to change the format of the output message.'
