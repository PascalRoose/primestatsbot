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

from telegram.ext import Updater, PicklePersistence

from primestatsbot.configurations.settings import TOKEN, NAME
from primestatsbot.history import save_history
from primestatsbot.chatsettings import save_chatsettings
from primestatsbot.utils.logger import init_logger
from primestatsbot.utils.utils import load_handlers, load_jobs


def run():
    """Run the telegram bot"""
    # Initialize the logger
    log_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), f'logs/{NAME}.log')
    init_logger(log_path)

    # Persistence file
    picklepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources/telegram.pickle')
    persistence = PicklePersistence(filename=picklepath)

    # Create the Updater with the bottoken saved in .env
    updater = Updater(TOKEN, use_context=True, persistence=persistence)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    load_handlers(dispatcher)

    # Load jobs into the jobqueue
    job_queue = updater.job_queue
    load_jobs(job_queue)

    # Start the Bot
    updater.start_polling()

    # Run the handlers until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the handlers gracefully.
    updater.idle()

    # Make sure to save history and usersettings before shutting down
    save_history()
    save_chatsettings()
