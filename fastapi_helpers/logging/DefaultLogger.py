from .ColoredFormater import ColoredFormatter
import watchtower
import logging
from ..settings.DefaultSettings import DefaultSettings
from .AwsLogFormatter import AwsLogFormatter
from typing import List

RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"


def formatter_message(message):
    m = message.replace(
        "$RESET", RESET_SEQ
    )
    return m


class DefaultLogger(logging.Logger):

    FORMAT = "%(levelname)s: %(message)s \t(%(pathname)s Line:%(lineno)d$RESET)"
    COLOR_FORMAT = formatter_message(FORMAT)
    NONE_FORMAT = "%(levelname)s: %(message)s"
    
    def __init__(
        self,
        name,
        settings: DefaultSettings = None,
        log_format=None,
    ):
        super().__init__(f"{name}")
        self.addHandler(self.get_handler_logger(settings, log_format))

    @classmethod
    def get_handler_logger(
            cls, 
            settings: DefaultSettings = None, 
            log_format:str=None,
            use_queues:bool = True,
            log_record_attrs: List[str]=[
                "pathname", 
                "lineno"
            ]
        ) -> logging.Handler:
        handler = None
        if(settings is not None and settings.is_production()):
            if(log_format is None):
                log_format = cls.NONE_FORMAT
            handler = watchtower.CloudWatchLogHandler(
                log_group_name=settings.app_name,
                use_queues=use_queues,
            )
            aws_formatter = AwsLogFormatter(log_format)
            handler.setFormatter(aws_formatter)
            handler.formatter.add_log_record_attrs=log_record_attrs
        else:
            if(log_format is None):
                log_format = cls.COLOR_FORMAT
            color_formatter = ColoredFormatter(log_format)
            handler = logging.StreamHandler()
            handler.setFormatter(color_formatter)
        return handler
