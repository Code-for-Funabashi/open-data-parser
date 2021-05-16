""" logger """

import sys
import logging


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

stream = logging.StreamHandler(stream=sys.stderr)
stream.setFormatter(formatter)

logger = logging.getLogger("open-data-parser")
logger.setLevel(logging.INFO)
logger.addHandler(stream)
