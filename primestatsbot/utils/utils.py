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

import os
from importlib import import_module

from primestatsbot.utils.logger import get_logger

LOGGER = get_logger(__name__)


def load_handlers(dispatcher):
    """Load handlers from the files in the 'handlers' directory"""
    LOGGER.debug('Loading handlers')

    base_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../handlers')
    files = os.listdir(base_path)

    # Make sure not to include __pycache__
    try:
        files.remove('__pycache__')
    # ValueError is raised if __pycache__ doens't exist, ignore
    except ValueError:
        pass

    for file_name in files:
        handler_module, _ = os.path.splitext(file_name)

        module = import_module(f'.{handler_module}', 'primestatsbot.handlers')
        module.init(dispatcher)


def load_jobs(job_queue):
    """Load jobs from the files in the 'jobs' directory"""
    LOGGER.debug('Loading jobs')

    base_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../jobs')
    files = os.listdir(base_path)

    # Make sure not to include __pycache__
    try:
        files.remove('__pycache__')
    # ValueError is raised if __pycache__ doens't exist, ignore
    except ValueError:
        pass

    for file_name in files:
        job_module, _ = os.path.splitext(file_name)

        module = import_module(f'.{job_module}', 'primestatsbot.jobs')
        module.init(job_queue)
