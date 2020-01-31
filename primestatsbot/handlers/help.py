#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ** Stats Converter **
# This is a simple Telegram bot for converting exported stats from Ingress Prime to a nicely formatted message
#
# - Author: PascalRoose
# - Repo: https://github.com/PascalRoose/primestatsbot.git
#

from telegram import Update, ParseMode
from telegram.ext import CallbackContext, CommandHandler, Dispatcher, run_async

from primestatsbot.configurations.messages import HELP_MESSAGE


def init(dispatcher: Dispatcher):
    dispatcher.add_handler(CommandHandler(command='help', callback=command_help))


@run_async
def command_help(update: Update, _context: CallbackContext):
    """Send a help message when a user sends /help"""
    update.message.reply_text(HELP_MESSAGE, parse_mode=ParseMode.MARKDOWN)
