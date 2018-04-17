"""
Python client to the EPICS Archiver Appliance.
"""
import logging
import tzlocal


SCAN = 'SCAN'
MONITOR = 'MONITOR'

# Make local timezone easy to get hold of.
LOCALTZ = tzlocal.get_localzone()

# Logging utilities
LOG_FORMAT = '%(asctime)s %(levelname)-8s %(message)s'
LOG_LEVEL = logging.DEBUG


def set_up_logging(format=LOG_FORMAT, level=LOG_LEVEL):
    logging.basicConfig(
        format=format, level=level, datefmt='%Y-%m-%d %I:%M:%S'
    )
