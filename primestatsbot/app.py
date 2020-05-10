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

from appdirs import user_log_dir, user_cache_dir

import telegram.bot
from telegram.ext import messagequeue as mq
from telegram.ext import Updater, PicklePersistence
from telegram.utils.request import Request

from primestatsbot.configurations.settings import TOKEN, NAME
from primestatsbot.utils.logger import init_logger
from primestatsbot.utils.utils import load_handlers, load_jobs


class MQBot(telegram.bot.Bot):
    # A subclass of Bot which delegates send method handling to MQ
    def __init__(self, *args, is_queued_def=True, mqueue=None, **kwargs):
        super(MQBot, self).__init__(*args, **kwargs)
        # below 2 attributes should be provided for decorator usage
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mqueue or mq.MessageQueue()

    def __del__(self):
        try:
            self._msg_queue.stop()
        except:
            pass

    @mq.queuedmessage
    def send_message(self, *args, **kwargs):
        # Wrapped method would accept new `queued` and `isgroup` OPTIONAL arguments
        return super(MQBot, self).send_message(*args, **kwargs)


def run():
    """Run the telegram bot"""

    # Initialize the logger
    logfile = os.path.join(user_log_dir("primestatsbot"), f'{NAME}.log')
    init_logger(logfile)

    # Telegram persistence file
    picklefile = os.path.join(user_cache_dir("primestatsbot"), "telegram.pickle")
    persistence = PicklePersistence(filename=picklefile)

    mqueue = mq.MessageQueue(all_burst_limit=10, all_time_limit_ms=3000)
    request = Request(con_pool_size=8)

    tgbot = MQBot(TOKEN, request=request, mqueue=mqueue)

    # Create the Updater with the bottoken saved in .env
    updater = Updater(bot=tgbot, use_context=True, persistence=persistence)

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
