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

from emoji import emojize
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, Chat
from telegram.ext import (Dispatcher, CallbackContext, CommandHandler, CallbackQueryHandler, ConversationHandler,
                          run_async)

from primestatsbot.messages import SETTINGS_MESSAGE
from primestatsbot.chatsettings import Copymode, chatsettings, add_chatsettings

# Conversation states
HOME, STATS, COPY = range(3)

# Callback data for switching states
GO_HOME, GO_STATS, GO_COPY = range(3)


def init(dispatcher: Dispatcher):
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('settings', show_settings)],
        states={
            HOME: [CallbackQueryHandler(set_headers, pattern='^headers$'),
                   CallbackQueryHandler(set_units, pattern='^units$'),
                   CallbackQueryHandler(go_stats, pattern='^' + str(GO_STATS) + '$'),
                   CallbackQueryHandler(go_copy, pattern='^' + str(GO_COPY) + '$')],
            COPY: [CallbackQueryHandler(go_home, pattern='^' + str(GO_HOME) + '$'),
                   CallbackQueryHandler(set_copy, pattern='^cp_')],
            STATS: [CallbackQueryHandler(go_home, pattern='^' + str(GO_HOME) + '$'),
                    CallbackQueryHandler(go_stats, pattern='^' + str(GO_STATS) + '$'),
                    CallbackQueryHandler(go_cat, pattern='^cat_'),
                    CallbackQueryHandler(set_stat, pattern='^stat_')]
        },
        fallbacks=[CommandHandler('settings', show_settings)],
        per_message=False
    )
    dispatcher.add_handler(conv_handler)


def _allowed(update: Update):
    if update.effective_chat.type == Chat.GROUP or update.effective_chat.type == Chat.SUPERGROUP:
        admins = update.effective_chat.get_administrators()
        for admin in admins:
            if update.effective_user.id == admin.user.id:
                return True
    elif update.effective_chat.type == Chat.PRIVATE:
        return True
    return False


def home_keyboard(chat_id: int):
    """Keyboard for home state"""
    # give copymode a nice name for output
    if chatsettings[chat_id]["copy"] == Copymode.NONE.value:
        copymode = 'None'
    elif chatsettings[chat_id]["copy"] == Copymode.VALUES_ONLY.value:
        copymode = 'Values'
    elif chatsettings[chat_id]["copy"] == Copymode.NAME_AND_VALUE.value:
        copymode = 'Name and value'
    else:
        copymode = 'All'

    # Checkmark if true, red cross if false
    if chatsettings[chat_id]["headers"]:
        headers = emojize(":white_check_mark:", use_aliases=True)
    else:
        headers = emojize(":x:", use_aliases=True)

    # Checkmark if true, red X if false
    if chatsettings[chat_id]["units"]:
        units = emojize(":white_check_mark:", use_aliases=True)
    else:
        units = emojize(":x:", use_aliases=True)

    keyboard = [
        [InlineKeyboardButton(text=f'Show headers: {headers}', callback_data=f'headers')],
        [InlineKeyboardButton(text=f'Show units: {units}', callback_data=f'units')],
        [InlineKeyboardButton(text=f'Show/hide stats', callback_data=str(GO_STATS))],
        [InlineKeyboardButton(text=f'Copymode: {copymode}', callback_data=str(GO_COPY))]
    ]
    return InlineKeyboardMarkup(keyboard)


def stats_keyboard(chat_id: int):
    """Keyboard for stats state"""
    keyboard = []

    for cat, stats in chatsettings[chat_id]['stats'].items():
        # Checkmark if show_stat is true for all stats in the category
        if all(value is True for _, value in stats.items()):
            icon = emojize(":white_check_mark: ", use_aliases=True)
        # Red X if show_stat is false for all stats in the category
        elif all(value is False for _, value in stats.items()):
            icon = emojize(":x: ", use_aliases=True)
        # Else a minus-emoji
        else:
            icon = emojize(":heavy_minus_sign:")
        keyboard.append([InlineKeyboardButton(text=f'{icon}{cat}', callback_data=f'cat_{cat}_all')])

    # Back button to go to the home state
    keyboard.append([InlineKeyboardButton(text=emojize(':arrow_left:', use_aliases=True), callback_data=str(GO_HOME))])

    return InlineKeyboardMarkup(keyboard)


def cat_keyboard(chat_id: int, cat: str):
    """Keyboard with all stats within a category to disable or enable"""
    keyboard = []

    # Buttons in one row. Enable all (checkmark), disable all (red X)
    enable_disable = [
        InlineKeyboardButton(text=emojize(":white_check_mark: ", use_aliases=True),
                             callback_data=f'stat_{cat}_en-all'),
        InlineKeyboardButton(text=emojize(":x: ", use_aliases=True),
                             callback_data=f'stat_{cat}_dis-all')
    ]
    keyboard.append(enable_disable)

    # Add every stat in the category to the keyboard as button
    for stat_name, show in chatsettings[chat_id]['stats'][cat].items():
        if show:
            icon = emojize(":white_check_mark: ", use_aliases=True)
        else:
            icon = emojize(":x: ", use_aliases=True)
        keyboard.append([InlineKeyboardButton(text=f'{icon}{stat_name}',
                                              callback_data=f'stat_{cat}_{stat_name}')])
    keyboard.append([InlineKeyboardButton(text=emojize(':arrow_left:', use_aliases=True),
                                          callback_data=str(GO_STATS))])

    return InlineKeyboardMarkup(keyboard)


def copy_keyboard(chat_id: int):
    """Keyboard for copy state"""

    # Icons for indicating the current copymode (radio-button)
    copymode = chatsettings[chat_id]['copy']
    icons = [
        (emojize(':radio_button:', use_aliases=True) if copymode == Copymode.NONE.value
         else emojize(':black_circle:', use_aliases=True)),
        (emojize(':radio_button:', use_aliases=True) if copymode == Copymode.VALUES_ONLY.value
         else emojize(':black_circle:', use_aliases=True)),
        (emojize(':radio_button:', use_aliases=True) if copymode == Copymode.NAME_AND_VALUE.value
         else emojize(':black_circle:', use_aliases=True)),
        (emojize(':radio_button:', use_aliases=True) if copymode == Copymode.ALL.value
         else emojize(':black_circle:', use_aliases=True)),
    ]

    keyboard = [
        [InlineKeyboardButton(text=f'{icons[0]} No copy mode', callback_data=f'cp_{Copymode.NONE.value}')],
        [InlineKeyboardButton(text=f'{icons[1]} Only values', callback_data=f'cp_{Copymode.VALUES_ONLY.value}')],
        [InlineKeyboardButton(text=f'{icons[2]} Name and value', callback_data=f'cp_{Copymode.NAME_AND_VALUE.value}')],
        [InlineKeyboardButton(text=f'{icons[3]} All text', callback_data=f'cp_{Copymode.ALL.value}')],
        [InlineKeyboardButton(text=emojize(':arrow_left:', use_aliases=True), callback_data=str(GO_HOME))]
    ]

    return InlineKeyboardMarkup(keyboard)


@run_async
def show_settings(update: Update, _context: CallbackContext):
    """Show settings message with menu (inline keyboard) upon command"""
    if _allowed(update):
        # Make sure chat_id is in chatsettings
        chat_id = update.effective_chat.id
        if chat_id not in chatsettings:
            add_chatsettings(chat_id)

        reply_markup = home_keyboard(chat_id)
        update.message.reply_text(SETTINGS_MESSAGE, reply_markup=reply_markup)

        return HOME
    return ConversationHandler.END


@run_async
def go_home(update: Update, _context: CallbackContext):
    """Switch to home state, update the keyboard"""
    if _allowed(update):
        query = update.callback_query
        chat_id = query.message.chat.id

        reply_markup = home_keyboard(chat_id)

        query.edit_message_reply_markup(reply_markup)
        query.answer()

        return HOME


@run_async
def go_stats(update: Update, _context: CallbackContext):
    """Switch to stats state, update the keyboard"""
    if _allowed(update):
        query = update.callback_query
        chat_id = query.message.chat.id

        reply_markup = stats_keyboard(chat_id)

        query.edit_message_reply_markup(reply_markup)
        query.answer()

        return STATS


@run_async
def go_cat(update: Update, _context: CallbackContext):
    """Update the keyboard to the right category"""
    if _allowed(update):
        query = update.callback_query
        chat_id = query.message.chat.id
        _, cat, _ = query.data.split('_')

        reply_markup = cat_keyboard(chat_id, cat)

        query.edit_message_reply_markup(reply_markup)
        query.answer()

        return STATS


@run_async
def go_copy(update: Update, _context: CallbackContext):
    """Switch to copy state, update the keyboard"""
    if _allowed(update):
        query = update.callback_query
        chat_id = query.message.chat.id

        reply_markup = copy_keyboard(chat_id)

        query.edit_message_reply_markup(reply_markup)
        query.answer()

        return COPY


@run_async
def set_headers(update: Update, context: CallbackContext):
    """Change the header setting"""
    if _allowed(update):
        query = update.callback_query
        chat_id = query.message.chat.id

        if chatsettings[chat_id]['headers']:
            chatsettings[chat_id]['headers'] = False
        else:
            chatsettings[chat_id]['headers'] = True

        return go_home(update, context)


@run_async
def set_units(update: Update, context: CallbackContext):
    """Change the units setting"""
    if _allowed(update):
        query = update.callback_query
        chat_id = query.message.chat.id

        if chatsettings[chat_id]['units']:
            chatsettings[chat_id]['units'] = False
        else:
            chatsettings[chat_id]['units'] = True

        return go_home(update, context)


@run_async
def set_stat(update: Update, context: CallbackContext):
    """Change the stats setting"""
    if _allowed(update):
        query = update.callback_query
        chat_id = query.message.chat.id

        _, cat, stat = query.data.split('_')

        # If en-all set all stats in the category to true
        if stat == 'en-all':
            for stat, _ in chatsettings[chat_id]['stats'][cat].items():
                chatsettings[chat_id]['stats'][cat][stat] = True
        # Else if dis-all set all stats in the category to false
        elif stat == 'dis-all':
            for stat, _ in chatsettings[chat_id]['stats'][cat].items():
                chatsettings[chat_id]['stats'][cat][stat] = False
        # Else switch setting for individual stat
        else:
            if chatsettings[chat_id]['stats'][cat][stat]:
                chatsettings[chat_id]['stats'][cat][stat] = False
            else:
                chatsettings[chat_id]['stats'][cat][stat] = True

        return go_cat(update, context)


@run_async
def set_copy(update: Update, context: CallbackContext):
    """Change the copy setting"""
    if _allowed(update):
        query = update.callback_query
        _, copymode = query.data.split('_')
        chat_id = query.message.chat.id

        # If the setting stays the same, return to state COPY, do not update
        if chatsettings[chat_id]['copy'] == int(copymode):
            query.answer()
            return COPY

        # Update setting, refresh keyboard
        chatsettings[chat_id]['copy'] = int(copymode)
        return go_copy(update, context)
