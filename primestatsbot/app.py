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

from appdirs import user_log_dir, user_cache_dir
from telegram.ext import Updater, PicklePersistence

from primestatsbot.configurations.settings import TOKEN, NAME
from primestatsbot.utils.logger import init_logger
from primestatsbot.utils.utils import load_handlers, load_jobs


def run():
    """Run the telegram bot"""

    # Initialize the logger
    logfile = os.path.join(user_log_dir("primestatsbot"), f'{NAME}.log')
    init_logger(logfile)

    # Telegram persistence file
    picklefile = os.path.join(user_cache_dir("primestatsbot"), "telegram.pickle")
    persistence = PicklePersistence(filename=picklefile)

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
