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
from telegram.ext import Dispatcher, CallbackContext, MessageHandler, run_async

from primestatsbot.utils.exceptions import IncorrectMessageError
from primestatsbot.resources.history import add_record
from primestatsbot.configurations.messages import INCORRECT_MESSAGE
from primestatsbot.resources.primestats import PRIMESTATS
from primestatsbot.resources.chatsettings import chatsettings, add_chatsettings, update_chatsettings
from primestatsbot.utils import converter
from primestatsbot.utils.filters import StatsFilter


def init(dispatcher: Dispatcher):
    dispatcher.add_handler(MessageHandler(filters=StatsFilter(), callback=convert_primestats))


@run_async
def convert_primestats(update: Update, context: CallbackContext):
    """Convert primestats message to something readable using the chatsettings"""
    try:
        message = update.message.text
        stats_dict = converter.process_stats(message)
        chat_id = update.effective_chat.id

        add_record(chat_id)

        stats_message = ''

        # Add the user to chatsettings if user wasn't in it yet
        if chat_id not in chatsettings:
            add_chatsettings(chat_id)

        # Get the chatsettings
        headers = chatsettings[chat_id]['headers']
        copymode = chatsettings[chat_id]['copy']
        show_unit = chatsettings[chat_id]['units']
        show_stat = chatsettings[chat_id]['stats']

        # If copy mode is 3 (All) wrap the entire message with `backticks`
        if copymode == 3:
            stats_message += '`'

        # Loop through all categories
        for category, stats in stats_dict.items():
            # If not all (so some not) stats in a category were set to hidden, loop through the category
            #  else all categories were set to hidden, so skip this category
            if not all(value is False for _, value in show_stat[category].items()):
                # Only add headers to the message if enabled in chatsettings
                if headers:
                    # Add newline (\n) before category if it's not the on the first line (start of the message)
                    if len(stats_message.split('\n')) > 0:
                        stats_message += '\n'
                    stats_message += f'{category}\n'
                # Loop through the stats in the category
                for stat_name, stat_value in stats.items():
                    # Add the stat to chatsettings if the key was not found
                    if stat_name not in show_stat[category]:
                        show_stat[category][stat_name] = True
                        update_chatsettings(chat_id, chatsettings[chat_id])

                    # Only add the stat to the message if it's enabled in chatsettings
                    if show_stat[category][stat_name]:
                        # Get the unit associated with the stat
                        unit = PRIMESTATS[category][stat_name]

                        # If copymode is 0 (None) or 3 (All) don't use `backticks`
                        if copymode == 0 or copymode == 3:
                            stats_message += f'{stat_name}: {stat_value}{" " + unit if show_unit else ""}\n'
                        # Else if copymode is 1 (values only) wrap the value (and unit) in `backticks`
                        elif copymode == 1:
                            stats_message += f'{stat_name}: `{stat_value}{" " + unit if show_unit else ""}`\n'
                        # Else if copymode is 2 (name and value) wrap the entire line in `backticks`
                        elif copymode == 2:
                            stats_message += f'`{stat_name}: {stat_value}{" " + unit if show_unit else ""}`\n'

        # If copy mode is 3 (All) wrap the entire message with `backticks`
        if copymode == 3:
            stats_message += '`'

        update.message.reply_text(stats_message, parse_mode=ParseMode.MARKDOWN)

    except IncorrectMessageError:
        return incorrect_message(update, context)


@run_async
def incorrect_message(update: Update, _context: CallbackContext):
    """Let the user know when the primestat message could not be converted, likely because the message was corrupted"""
    update.message.reply_text(INCORRECT_MESSAGE, parse_mode=ParseMode.MARKDOWN)
