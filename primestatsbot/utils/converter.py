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

from primestatsbot.exceptions import IncorrectMessageError
from primestatsbot.primestats import PRIMESTATS


def _fix_timespan(stats_values):
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


def process_stats(message):
    """Convert the exported stats to a dictionary"""
    # Check if there are is only one linebreak (so two lines). If not the message format is incorrect
    if len(str(message).split('\n')) != 2:
        raise IncorrectMessageError

    # Split first row (keys) and second row (values). Use only the second row (values) and split at every space
    # We now have a list of all values. Timespan needs to be fixed first, see the function above for explaination.
    stats_values = _fix_timespan(str(message).split('\n')[1].split(' '))

    # Init a dictionary. This will represent the name of the stats as key, and the value of the stat as value.
    stats_dict = {}

    # Create an index to keep track of the element we're  at
    stats_index = 0

    # Loop through the every category in stats_header.
    # Event stats that a player doesn't have will not be shown in the export, that's why we have to check
    for category, stats in PRIMESTATS.items():
        # Loop through all stats in this category. For each stat check if it's in the export.
        for name, unit in stats.items():
            if name in message:
                # Add the category to the stats_dict (if that didn't happen yet)
                if category not in stats_dict:
                    stats_dict[category] = {}
                # If the value is a number add comma's for every thousand (readability)
                try:
                    value = stats_values[stats_index]
                # If the index does not exist this means the message is incomplete and thus incorrect
                except IndexError:
                    raise IncorrectMessageError
                # If the value is a digit convert it to a string with comma seperators for thousands
                if value.isdigit():
                    value = '{:,}'.format(int(value))
                # Add the name and value (with unit) of the stat to the dictionary
                stats_dict[category][name] = f'{value}'
                # Up the index by 1, next!
                stats_index += 1

    return stats_dict
