#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ** Stats Converter **
# This is a simple Telegram bot for converting exported stats from Ingress Prime to a nicely formatted message
#
# - Author: PascalRoose
# - Repo: https://github.com/PascalRoose/primestatsbot.git
#

from telegram import Update, Chat
from telegram.ext import Dispatcher, CommandHandler, CallbackContext

from primestatsbot.configurations.settings import ADMIN
from primestatsbot.resources.history import get_usage_total, get_usage_week, get_users_total, get_users_week


def init(dispatcher: Dispatcher):
    dispatcher.add_handler(CommandHandler(command='stats', callback=stats_command))


def stats_command(update: Update, _context: CallbackContext):
    """Return statistics upon command from admin in private chat"""
    if update.effective_user.id == ADMIN and update.effective_chat.type == Chat.PRIVATE:
        usage_week = get_usage_week()
        usage_total = get_usage_total()
        users_week = get_users_week()
        users_total = get_users_total()

        message = f'Usage this week: {usage_week}\n' \
                  f'Total usage: {usage_total}\n\n' \
                  f'Unique users this week: {users_week}\n' \
                  f'Total unique users: {users_total}'

        update.message.reply_text(message)
