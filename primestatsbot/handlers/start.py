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
from telegram.ext import CallbackContext, CommandHandler, Dispatcher, MessageHandler, Filters, run_async

from primestatsbot.configurations.settings import NAME
from primestatsbot.configurations.messages import START_MESSAGE, JOIN_MESSAGE


def init(dispatcher: Dispatcher):
    dispatcher.add_handler(CommandHandler(command='start', callback=command_start))
    dispatcher.add_handler(MessageHandler(filters=Filters.status_update.chat_created, callback=on_chatcreated))
    dispatcher.add_handler(MessageHandler(filters=Filters.status_update.new_chat_members, callback=on_joinchat))


@run_async
def command_start(update: Update, _context: CallbackContext):
    """Send a start message when a user sends /start"""
    update.message.reply_text(START_MESSAGE, parse_mode=ParseMode.MARKDOWN)


@run_async
def on_chatcreated(update: Update, _context: CallbackContext):
    """Send a message when a new chat is created with the bot"""
    update.message.reply_text(JOIN_MESSAGE, parse_mode=ParseMode.MARKDOWN)


@run_async
def on_joinchat(update: Update, _context: CallbackContext):
    """Send a message when the bot gets added to a group"""
    # Check if the member that was added is the handlers itself
    for member in update.message.new_chat_members:
        if member.name == f'@{NAME}':
            update.message.reply_text(JOIN_MESSAGE, parse_mode=ParseMode.MARKDOWN)
