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

from configparser import ConfigParser
from appdirs import user_config_dir

configfile = os.path.join(user_config_dir("primestatsbot"), 'config.ini')


def run():
    """Setup config.ini"""
    print('Running configuration setup')

    config = ConfigParser()

    config['DEFAULT']['Token'] = input('Bot token: ')
    config['DEFAULT']['Name'] = input('Name of the bot (without @): ')
    config['DEFAULT']['Admin'] = input('Admin Telegram ID: ')

    enable_webhook = input('Do you want to enable updates over webhook? [y/N] ')

    if enable_webhook == 'y' or enable_webhook == 'Y':
        config['Webhook']['Enabled'] = 'true'
        config['Webhook']['IP'] = input('IP address: ')
        config['Webhook']['Port'] = input('Port number: ')
        config['Webhook']['Path'] = input('Path (bot token as path is recommended): ')
        config['Webhook']['URL'] = input('URL (eg. https://example.com/path): ')
    else:
        config['Webhook'] = {
            'Enabled': 'false',
            'IP': '0.0.0.0',
            'Port': 443,
            'Path': config['DEFAULT']['Token'],
            'URL': f'https://example.com/{config["DEFAULT"]["Token"]}'
        }

    with open(configfile, 'w+') as configfile_out:
        config.write(configfile_out)
