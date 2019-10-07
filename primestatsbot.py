#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- style: pep-8 -*-
#
# ** Stats Converter **
# This is a simple Telegram bot for converting exported stats from Ingress Prime to human readable text
#
# - Author: PascalRoose
# - Repo: https://github.com/PascalRoose/primestatsbot.git
#

import os
import logging

from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, BaseFilter
from dotenv import load_dotenv

# Enable logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load .env file
load_dotenv()

# All possible stats in the order it would appear in the export
stats_header = \
    {
        # Categories
        'General': {
            # 'Stat name' : 'Unit'
            'Time Span': '',
            'Agent Name': '',
            'Agent Faction': '',
            'Date (yyyy-mm-dd)': '',
            'Time (hh:mm:ss)': '',
            'Level': '',
            'Lifetime AP': 'AP',
            'Current AP': 'AP'
        },
        'Discovery': {
            'Unique Portals Visited': '',
            'Portals Discovered': '',
            'Seer Points': '',
            'XM Collected': 'XM',
            'OPR Agreements': ''
        },
        'Health': {
            'Distance Walked': 'km'
        },
        'Building': {
            'Resonators Deployed': '',
            'Links Created': '',
            'Control Fields Created': '',
            'Mind Units Captured': 'MUs',
            'Longest Link Ever Created': 'km',
            'Largest Control Field': 'MUs',
            'XM Recharged': '',
            'Portals Captured': '',
            'Unique Portals Captured': '',
            'Mods Deployed': '',
            'Links Active': '',
            'Portals Owned': '',
            'Control Fields Active': '',
            'Mind Unit Control': 'MUs'
        },
        'Combat': {
            'Resonators Destroyed': '',
            'Portals Neutralized': '',
            'Enemy Links Destroyed': '',
            'Enemy Fields Destroyed': ''
        },
        'Defense': {
            'Max Time Portal Held': 'days',
            'Max Time Link Maintained': 'days',
            'Max Link Length x Days': 'km-days',
            'Max Time Field Held': 'days',
            'Largest Field MUs x Days': 'MU-days'
        },
        'Missions': {
            'Unique Missions Completed': ''
        },
        'Resource Gathering': {
            'Hacks': '',
            'Glyph Hack Points': '',
            'Longest Hacking Streak': 'days',
            'Current Hacking Streak': 'days'
        },
        'Mentoring': {
            'Agents Successfully Recruited': ''
        },
        'Events': {
            'Mission Day(s) Attended': '',
            'NL-1331 Meetup(s) Attended': '',
            'First Saturday Events': '',
            'Clear Fields Events': '',
            'OPR Live Events': '',
            'Prime Challenges': '',
            'Intel Ops Missions': '',
            'Stealth Ops Missions': ''
        },
        'Recursion': {
            'Recursions': ''
        }
    }


# Custom filter to check if a 'exported stats' message was sent
class StatsFilter(BaseFilter):
    def filter(self, message):
        # Check if the message contains at least the first 7 keys in stats_header (# General)
        return str(message.text).startswith(' '.join(stats_header['General'].keys()))


def fix_timespan(stats_values):
    # Everything in the export gets translated to English EXCEPT the value of timespan /rage

    # In some languages ALL TIME is translated to one or more words.
    # WEEK, MONTH, NOW might be as well, but I'm sure about that...

    # The next bit is gonna find the value for timespan, if . It's a bit of a messy workaround, so hold tight

    # stats_values contains all of the values/words in the second line of the export message.
    # The third element is Faction (either Enlightened or Resistance). Depending on the translation of ALL TIME it's
    # either the 3rd, 4rd or maybe even 5th element in stats_values.
    if 'Enlightened' in stats_values:
        faction_index = stats_values.index('Enlightened')
    else:
        faction_index = stats_values.index('Resistance')

    # Agentname is the element before faction_index
    agentname_index = faction_index - 1

    # Contaminate the values of index 0 untill (not including) the index of agentname
    stats_values[0:agentname_index] = [' '.join(stats_values[0:agentname_index])]

    # Return the fixed stats_values array
    return stats_values


# Convert the exported stats to a nicely formatted message and send it
def process_stats(update, context):
    # Check if there are is only one linebreak (so two lines). If not the message format is incorrect
    if len(str(update.message.text).split('\n')) == 2:
        return process_incorrectmessage(update, context)

    # Split first row (keys) and second row (values). Use only the second row (values) and split at every space
    # We now have a list of all values. Timespan needs to be fixed first, see the function above for explaination.
    stats_values = fix_timespan(str(update.message.text).split('\n')[1].split(' '))

    # Init a dictionary. This will represent the name of the stats as key, and the value of the stat as value.
    stats_dict = {}

    # Create an index to keep track of the element we're  at
    stats_index = 0

    # Loop through the every category in stats_header.
    # Event stats that a player doesn't have will not be shown in the export, that's why we have to check
    for category, stats in stats_header.items():
        # Loop through all stats in this category. For each stat check if it's in the export.
        for name, unit in stats.items():
            if name in update.message.text:
                # Add the category to the stats_dict (if that didn't happen yet)
                if category not in stats_dict:
                    stats_dict[category] = {}
                # If the value is a number add comma's for every thousand (readability)
                try:
                    value = stats_values[stats_index]
                # If the index does not exist this means the message is incomplete and thus incorrect
                except IndexError:
                    return process_incorrectmessage(update, context)
                # If the value is a digit convert it to a string with comma seperators for thousands
                if value.isdigit():
                    value = '{:,}'.format(int(value))
                # Add the name and value (with unit) of the stat to the dictionary
                stats_dict[category][name] = f'{value} {unit}'
                # Up the index by 1, next!
                stats_index += 1

    # Generate the message that's going to be send back
    stats_message = ''
    # Loop through the categories in the dictionary
    for category, stats in stats_dict.items():
        # Print the name of the category in bold (Markdown)
        stats_message += f'\n*{category}*\n'
        # Loop through all stats in this category. Add every stat as a row to the output message.
        for name, value in stats.items():
            stats_message += f'{name}: {value}\n'

    # Send the generated message back
    update.message.reply_text(stats_message, parse_mode='Markdown')


def process_incorrectmessage(update, _context):
    if update.message.chat.type == 'private':
        update.message.reply_text(os.getenv('INCORRECT_MESSAGE'), parse_mode='Markdown')


# Send a message to users that start or simply type 'start' in private
def command_start(update, _context):
    if update.message.chat.type == 'private':
        update.message.reply_text(os.getenv('START_MESSAGE'), parse_mode='Markdown')


# Send a message when a new chat is created with the bot in it
def on_chatcreated(update, _context):
    update.message.reply_text(os.getenv('JOIN_MESSAGE'), parse_mode='Markdown')


# Send a message when the bot gets added to a group
def on_joinchat(update, _context):
    # Check if the member that was added is the bot itself
    for member in update.message.new_chat_members:
        if member.name == os.getenv('BOTNAME'):
            update.message.reply_text(os.getenv('JOIN_MESSAGE'))


# Log Errors caused by Updates.
def error(update, _context):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the Updater with the bottoken saved in .env
    updater = Updater(os.getenv('TOKEN'), use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Handlers: what triggers the bot and how should it respond
    dp.add_handler(CommandHandler('start', command_start))
    dp.add_handler(MessageHandler(Filters.status_update.chat_created, on_chatcreated))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, on_joinchat))
    dp.add_handler(MessageHandler(StatsFilter(), process_stats))
    dp.add_handler(MessageHandler(~ StatsFilter(), process_incorrectmessage))
    # Log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
