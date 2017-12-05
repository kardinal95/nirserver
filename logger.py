import os
import logging
import logging.config


def make_logger():
    global logger
    logging.config.fileConfig(os.path.join('conf', 'logging.conf'))
    return logging.getLogger('simpleExample')


logger = make_logger()
