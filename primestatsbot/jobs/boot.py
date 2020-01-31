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

from telegram.error import Unauthorized, BadRequest
from telegram.ext import CallbackContext, JobQueue, run_async

from primestatsbot.configurations.settings import ADMIN
from primestatsbot.exceptions import AdminDidNotStartBotError, InvalidAdminError
from primestatsbot.utils.logger import get_logger

LOGGER = get_logger(__name__)


def init(job_queue: JobQueue):
    job_queue.run_once(callback=boot_job, when=1)


@run_async
def boot_job(context: CallbackContext):
    """Run job upon boot. Notify the user that the bot has been booted succesfully"""
    try:
        context.bot.send_message(ADMIN, 'Boot up successful. I\'m up and running!')
    except Unauthorized:
        LOGGER.error('Admin, please start the bot so I can send you messages')
        raise AdminDidNotStartBotError
    except BadRequest:
        LOGGER.error('Invalid ADMIN (telegram id). Please check configurations/settings.py')
        raise InvalidAdminError
