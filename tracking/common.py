import os
import time
import datetime
import cv2
import errno
import itertools
import pickle
import numpy as np
import logging
from functools import wraps

LOG_PREFIX = './logs'
APPNAME = 'meichu'

def str_date():
    return datetime.datetime.now().strftime('%Y%m%d_%H%M%S')


def check_path(path):
    print('check {}'.format(path))
    try:
        os.makedirs(path)  # Support multi-level
        print(path, ' created')
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
        # print(path, ' exists')


def setup_logger(appname=APPNAME, filename=None):
    check_path(LOG_PREFIX)

    logger = logging.getLogger(appname)
    logger.setLevel(logging.DEBUG)

    if not filename:
        filename = '{}/{}_{}.txt'.format(LOG_PREFIX, appname, datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))  # ex: 20190823_103813

    print('logger {} setup: {}'.format(appname, filename))

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)

    fh = logging.FileHandler(filename)
    fh.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s %(name)s [%(levelname)s] %(message)s')
    fh.setFormatter(formatter)
    console.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(console)

    return logger
