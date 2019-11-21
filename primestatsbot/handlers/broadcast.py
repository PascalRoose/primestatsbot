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

from telegram import Update, Chat, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import (Dispatcher, ConversationHandler, MessageHandler, CallbackQueryHandler,
                          CommandHandler, Filters, CallbackContext)

from primestatsbot.chatsettings import chatsettings
from primestatsbot.configurations.settings import ADMIN

# Conversation states
MSG, CONFIRM = range(2)


def init(dispatcher: Dispatcher):
    conv_handler = ConversationHandler(
        persistent=True,
        name='broadcast',
        entry_points=[CommandHandler('broadcast', start_broadcast)],
        states={
            MSG: [MessageHandler(filters=Filters.text, callback=confirm_broadcast)],
            CONFIRM: [CallbackQueryHandler(send_broadcast, pattern='^y$'),
                      CallbackQueryHandler(cancel_broadcast, pattern='^n$')]
        },
        fallbacks=[CommandHandler('cancel', cancel_broadcast)],
        per_message=False
    )
    dispatcher.add_handler(conv_handler)


def start_broadcast(update: Update, _context: CallbackContext):
    """Request the broadcast message"""
    if update.effective_user.id == ADMIN and update.effective_chat.type == Chat.PRIVATE:
        update.message.reply_text('Send me a message you\'d like to broadcast. Cancel by typing/clicking /cancel.')
        return MSG
    return ConversationHandler.END


def confirm_broadcast(update: Update, _context: CallbackContext):
    """Request confirmation for sending the broadcast message"""
    update.message.reply_text('Please confirm: Do you want to broadcast the following message?')

    keyboard = [
        [InlineKeyboardButton(text='Yes', callback_data='y'), InlineKeyboardButton(text='No', callback_data='n')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(update.message.text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)

    return CONFIRM


def send_broadcast(update: Update, context: CallbackContext):
    """Send the broadcast"""
    bot = context.bot
    message = update.callback_query.message.text

    bot.send_message(chat_id=ADMIN, text='Sending message to all users. This might take a while...')

    for tg_id, settings in chatsettings.items():
        bot.send_message(chat_id=tg_id, text=message, parse_mode=ParseMode.MARKDOWN)

    update.callback_query.answer()

    return ConversationHandler.END


def cancel_broadcast(update: Update, context: CallbackContext):
    """Cancel the broadcast"""
    bot = context.bot
    bot.send_message(chat_id=ADMIN, text='Broadcast canceled. Type /broadcast if you want to try again')

    if update.callback_query is not None:
        update.callback_query.answer()

    return ConversationHandler.END
