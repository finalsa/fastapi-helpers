from unittest import TestCase
import sys 
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from fastapi_helpers.logging import DefaultLogger


class TestException(Exception):

    def __init__(self):
        self.message = "Test Exception"

class TestLogging(TestCase):

    def test_logging(self):
        logger = DefaultLogger("logger")
        logger.info("information")
        logger.debug("debug")
        logger.error("error")
        try:
            raise TestException()
        except Exception as ex:
            logger.exception(ex)
        logger.warning("warning")
