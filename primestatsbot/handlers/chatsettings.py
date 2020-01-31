#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ** Stats Converter **
# This is a simple Telegram bot for converting exported stats from Ingress Prime to a nicely formatted message
#
# - Author: PascalRoose
# - Repo: https://github.com/PascalRoose/primestatsbot.git
#

from copy import deepcopy

from emoji import emojize
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, Chat
from telegram.ext import (Dispatcher, CallbackContext, CommandHandler, CallbackQueryHandler, run_async)

from primestatsbot.configurations.messages import SETTINGS_MESSAGE
from primestatsbot.resources.chatsettings import Copymode, chatsettings, add_chatsettings, save_chatsettings

# Conversation states
HOME, STATS, CAT, COPY = range(4)


def init(dispatcher: Dispatcher):
    dispatcher.add_handler(CommandHandler(command='settings', callback=show_settings))
    dispatcher.add_handler(CallbackQueryHandler(pattern='^NAV_', callback=navigate_menu))
    dispatcher.add_handler(CallbackQueryHandler(pattern='^SET_', callback=update_settings))


def _allowed(update: Update):
    if update.effective_chat.type == Chat.GROUP or update.effective_chat.type == Chat.SUPERGROUP:
        admins = update.effective_chat.get_administrators()
        for admin in admins:
            if update.effective_user.id == admin.user.id:
                return True
    elif update.effective_chat.type == Chat.PRIVATE:
        return True
    return False


def keyboard_home(chat_id: int):
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
        [InlineKeyboardButton(text=f'Show headers: {headers}',
                              callback_data=f'SET_HEADERS_{"OFF" if chatsettings[chat_id]["headers"] else "ON"}')],
        [InlineKeyboardButton(text=f'Show units: {units}',
                              callback_data=f'SET_UNITS_{"OFF" if chatsettings[chat_id]["units"] else "ON"}')],
        [InlineKeyboardButton(text=f'Show/hide stats',
                              callback_data=f'NAV_{str(STATS)}')],
        [InlineKeyboardButton(text=f'Copymode: {copymode}',
                              callback_data=f'NAV_{str(COPY)}')]
    ]
    return InlineKeyboardMarkup(keyboard)


def keyboard_stats(chat_id: int):
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
        keyboard.append([InlineKeyboardButton(text=f'{icon}{cat}', callback_data=f'NAV_{str(CAT)}|{cat}')])

    # Back button to go to the home state
    keyboard.append([InlineKeyboardButton(text=emojize(':arrow_left:', use_aliases=True),
                                          callback_data=f'NAV_{str(HOME)}')])

    return InlineKeyboardMarkup(keyboard)


def keyboard_cat(chat_id: int, cat: str):
    """Keyboard with all stats within a category to disable or enable"""
    keyboard = []

    # Buttons in one row. Enable all (checkmark), disable all (red X)
    enable_disable = [
        InlineKeyboardButton(text=emojize(":white_check_mark: ", use_aliases=True),
                             callback_data=f'SET_{cat}|ALL_ON'),
        InlineKeyboardButton(text=emojize(":x: ", use_aliases=True),
                             callback_data=f'SET_{cat}|ALL_OFF')
    ]
    keyboard.append(enable_disable)

    # Add every stat in the category to the keyboard as button
    for stat_name, show in chatsettings[chat_id]['stats'][cat].items():
        if show:
            icon = emojize(":white_check_mark: ", use_aliases=True)
        else:
            icon = emojize(":x: ", use_aliases=True)
        keyboard.append([InlineKeyboardButton(text=f'{icon}{stat_name}',
                                              callback_data=f'SET_{cat}|{stat_name}_'
                                                            f'{"OFF" if show else "ON"}')])
    keyboard.append([InlineKeyboardButton(text=emojize(':arrow_left:', use_aliases=True),
                                          callback_data=f'NAV_{str(STATS)}')])

    return InlineKeyboardMarkup(keyboard)


def keyboard_copy(chat_id: int):
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
        [InlineKeyboardButton(text=f'{icons[0]} No copy mode',
                              callback_data=f'SET_COPY_{Copymode.NONE.value}')],
        [InlineKeyboardButton(text=f'{icons[1]} Only values',
                              callback_data=f'SET_COPY_{Copymode.VALUES_ONLY.value}')],
        [InlineKeyboardButton(text=f'{icons[2]} Name and value',
                              callback_data=f'SET_COPY_{Copymode.NAME_AND_VALUE.value}')],
        [InlineKeyboardButton(text=f'{icons[3]} All text',
                              callback_data=f'SET_COPY_{Copymode.ALL.value}')],
        [InlineKeyboardButton(text=emojize(':arrow_left:', use_aliases=True),
                              callback_data=f'NAV_{str(HOME)}')]
    ]

    return InlineKeyboardMarkup(keyboard)


@run_async
def set_keyboard(query, keyboard, chat_id):
    """Attach a given keyboard to a message"""
    if keyboard == str(HOME):
        query.edit_message_reply_markup(keyboard_home(chat_id))
    elif keyboard == str(STATS):
        query.edit_message_reply_markup(keyboard_stats(chat_id))
    elif keyboard == str(COPY):
        query.edit_message_reply_markup(keyboard_copy(chat_id))
    else:
        _, cat = keyboard.split('|')
        query.edit_message_reply_markup(keyboard_cat(chat_id, cat))

    query.answer()


@run_async
def show_settings(update: Update, _context: CallbackContext):
    """Show settings message with menu (inline keyboard) upon command"""
    if _allowed(update):
        # Make sure chat_id is in chatsettings
        chat_id = update.effective_chat.id
        if chat_id not in chatsettings:
            add_chatsettings(chat_id)

        reply_markup = keyboard_home(chat_id)
        update.message.reply_text(SETTINGS_MESSAGE, reply_markup=reply_markup)


@run_async
def navigate_menu(update:  Update, _context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat.id

    _, keyboard = query.data.split('_')

    set_keyboard(query, keyboard, chat_id)


@run_async
def update_settings(update: Update, _context: CallbackContext):
    if _allowed(update):
        query = update.callback_query
        chat_id = query.message.chat.id
        old_settings = deepcopy(chatsettings[chat_id])
        _, stat, setting = query.data.split('_')

        if stat == 'HEADERS':
            if setting == 'ON':
                chatsettings[chat_id]['headers'] = True
            elif setting == 'OFF':
                chatsettings[chat_id]['headers'] = False
            save_chatsettings()
            return set_keyboard(query, str(HOME), chat_id)
        elif stat == 'UNITS':
            if setting == 'ON':
                chatsettings[chat_id]['units'] = True
            elif setting == 'OFF':
                chatsettings[chat_id]['units'] = False
            save_chatsettings()
            return set_keyboard(query, str(HOME), chat_id)
        elif stat == 'COPY':
            # Update setting, refresh keyboard
            chatsettings[chat_id]['copy'] = int(setting)
            if chatsettings[chat_id] != old_settings:
                save_chatsettings()
                return set_keyboard(query, str(COPY), chat_id)
            else:
                query.answer()
        else:
            cat, stat = stat.split('|')
            if stat == 'ALL':
                for _stat, _ in chatsettings[chat_id]['stats'][cat].items():
                    if setting == 'ON':
                        chatsettings[chat_id]['stats'][cat][_stat] = True
                    elif setting == 'OFF':
                        chatsettings[chat_id]['stats'][cat][_stat] = False
            else:
                if setting == 'ON':
                    chatsettings[chat_id]['stats'][cat][stat] = True
                elif setting == 'OFF':
                    chatsettings[chat_id]['stats'][cat][stat] = False

            if chatsettings[chat_id] != old_settings:
                save_chatsettings()
                return set_keyboard(query, f'{str(CAT)}|{cat}', chat_id)
            else:
                query.answer()
