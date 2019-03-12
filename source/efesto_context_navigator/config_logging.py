import os
import logging
import logging.config
import appdirs
import errno


def get_log_directory():
    '''Get log directory.

    Will create the directory (recursively) if it does not exist.

    Raise if the directory can not be created.
    '''
    user_data_dir = appdirs.user_data_dir('efesto_ftrack_plugins', 'efestolab')
    log_directory = os.path.join(user_data_dir, 'log')

    if not os.path.exists(log_directory):
        try:
            os.makedirs(log_directory)
        except OSError as error:
            if error.errno == errno.EEXIST and os.path.isdir(log_directory):
                pass
            else:
                raise

    return log_directory


def configure_logging(logger_name, log_level=logging.WARNING):
    '''Configure logging with given logger_name, and log_level'''
    efesto_debug = os.getenv('EFESTO_DEBUG', False)
    module_logging = log_level

    log_directory = get_log_directory()
    log_directory = os.environ.get('EFESTO_LOG_PATH', log_directory)
    logfile = os.path.join(log_directory, '{0}.log'.format(logger_name))

    if efesto_debug:
        module_logging = logging.DEBUG

    log_format = (
        '[%(asctime)s][%(levelname)s] %(name)s'
        ' %(filename)s:%(funcName)s:%(lineno)d | %(message)s'
    )

    logging_settings = {
        'version': 1,
        'disable_existing_loggers': True,

        'formatters': {
            'console': {
                'format': log_format,
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
            'file': {
                'format': log_format
            }
        },
        'handlers': {
            'console': {
                'level': logging._levelNames[module_logging],
                'class': 'logging.StreamHandler',
                'formatter': 'console',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'DEBUG',
                'formatter': 'file',
                'filename': logfile,
                'mode': 'a',
                'maxBytes': 10485760,
                'backupCount': 5,
            },
        },
        'loggers': {
            '': {
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'ftrack_connect': {
                'level': 'WARNING',
                'propagate': False,
            },
            'ftrack_api': {
                'level': 'INFO',
                'propagate': False,
            },
            'FTrackCore': {
                'level': 'INFO',
                'propagate': False,
            },
            'requests': {
                'level': 'WARNING',
                'propagate': False,
            },
            logger_name: {
                'level': module_logging,
                'propagate': True,
            },
        }
    }

    logging.config.dictConfig(logging_settings)
    logging.captureWarnings(True)
    logging.info('Saving log file to: {0}'.format(logfile))
