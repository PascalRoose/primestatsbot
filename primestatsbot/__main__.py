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
import sys

from appdirs import AppDirs

# Create the required directories
dirs = AppDirs("primestatsbot")
os.makedirs(dirs.user_cache_dir, exist_ok=True)
os.makedirs(dirs.user_config_dir, exist_ok=True)
os.makedirs(dirs.user_log_dir, exist_ok=True)

configfile = os.path.join(dirs.user_config_dir, 'config.ini')


def app():
    """Run the bot"""
    print('Starting the Telegram Bot')

    from primestatsbot import app
    app.run()


def configure():
    """Setup config.ini"""
    print('Running configuration setup')

    from primestatsbot import configure
    configure.run()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        # No arguments were given
        if not os.path.exists(configfile):
            print("Configuration file was not found")
            configure()
        app()
    elif len(sys.argv) == 2:
        # One additional argument was given
        if sys.argv[1] == 'configure':
            configure()
        else:
            print('Invalid argument')
    else:
        print('Too many arguments...')
