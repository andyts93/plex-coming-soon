import logging
import sys
import os
from logging.handlers import TimedRotatingFileHandler

LOG_FILE_NAME = os.path.dirname(__file__)+'/logs/log.log'

# set up formatting
formatter = logging.Formatter('[%(asctime)s] %(levelname)s (%(process)d) %(module)s:%(lineno)d %(message)s')

# set up logging to STDOUT for all levels WARNING and higher
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.WARNING)
sh.setFormatter(formatter)

# set up logging to a file for all levels DEBUG and higher
#fh = logging.FileHandler(LOG_FILE_NAME)
fh = TimedRotatingFileHandler(LOG_FILE_NAME, when="d", interval=1, backupCount=7)
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)

# create logger object
logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)
logger.addHandler(sh)
logger.addHandler(fh)

# shortcuts
debug = logger.debug
info = logger.info
warning = logger.warning
error = logger.error
critical = logger.critical