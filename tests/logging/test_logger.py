from unittest import TestCase
import sys 
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from fastapi_helpers.logging import DefaultLogger


class TestLogging(TestCase):

    def test_logging(self):
        logger = DefaultLogger("logger")
        logger.info("information")
        logger.debug("debug")
        logger.error("error")
        try:
            raise Exception("Test Exception")
        except Exception as ex:
            logger.exception(ex)
        logger.warning("warning")
