from copy import copy
from typing import Dict
from fastapi_better_logger import (AWS_DEFAULT_CONFIG, DEFAULT_CONFIG)
from fastapi_helpers.settings import DefaultSettings
from datetime import datetime
import sys
import os
import threading
import platform
import functools

TEST_CONFIGURATION = copy(DEFAULT_CONFIG)
DEV_CONFIGURATION = copy(DEFAULT_CONFIG)
DEFAULT_LOG_STREAM_NAME = "{machine_name}/{program_name}/{logger_name}/{process_id}"

@functools.lru_cache(maxsize=0)
def get_machine_name():
    return platform.node()

def get_stream_name(logger_name):
    return DEFAULT_LOG_STREAM_NAME.format(
        machine_name=get_machine_name(),
        program_name=sys.argv[0],
        process_id=os.getpid(),
        thread_name=threading.current_thread().name,
        logger_name=logger_name,
        strftime=datetime.utcnow()
    )

def get_logger_prod_config(settings: DefaultSettings) -> Dict:
    settings.env = "prod"
    PROD_CONFIGURATION = copy(AWS_DEFAULT_CONFIG)
    handlers = PROD_CONFIGURATION["handlers"]
    stream_name = get_stream_name(settings.app_name)
    for handler in handlers:
        PROD_CONFIGURATION["handlers"][handler]["stream_name"] = stream_name
        PROD_CONFIGURATION["handlers"][handler]["log_group_name"] = settings.app_name
    return PROD_CONFIGURATION



def get_logger_default_config(settings: DefaultSettings):
    if settings.is_production():
        return get_logger_prod_config(settings)
    elif settings.is_test():
        return TEST_CONFIGURATION
    return DEV_CONFIGURATION