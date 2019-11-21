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

from telegram import Update
from telegram.error import (TelegramError, Unauthorized, BadRequest, TimedOut,
                            NetworkError, ChatMigrated, Conflict, RetryAfter)
from telegram.ext import CallbackContext, Dispatcher, run_async

from primestatsbot.configurations.settings import ADMIN
from primestatsbot.utils.logger import get_logger

LOGGER = get_logger(__name__)


def init(dispatcher: Dispatcher):
    dispatcher.add_error_handler(error_handler)


@run_async
def error_handler(update: Update, context: CallbackContext):
    """Handle errors in an elegant way, notifying the admin of what happened"""
    error = context.error
    LOGGER.warning('Update "%s" caused error "%s"', update, error)
    try:
        raise error
    except TimedOut:
        update.effective_message.reply_text('Request timed out... Please try again')
    except NetworkError:
        # TODO: Handle other connection problems...
        return
    except (Unauthorized, TelegramError, BadRequest, ChatMigrated, Conflict, RetryAfter):
        pass
    finally:
        error_msg = f'Error found: {error}. Update: {update}'
        LOGGER.error(error_msg, exc_info=True)

        try:
            text = update.effective_message.text
            user = update.effective_user
            chat = update.effective_chat

            error_msg = (f'User: {user.name}\n\n'
                         f'Text:\n{text}\n\n'
                         f'Chat:\n'
                         f'- ID: {chat.id}\n'
                         f'- Type: {chat.type}\n'
                         f'- Name: {chat.title if chat.title is not None else user.full_name}\n\n'
                         f'Error: \n{repr(error)} - {str(error)}\n\n'
                         f'Check the log to  see the traceback')
        except Exception:
            pass

        context.bot.send_message(ADMIN, error_msg)
