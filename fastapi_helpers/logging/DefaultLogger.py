from .ColoredFormater import ColoredFormatter
import watchtower
import logging
from ..settings.DefaultSettings import DefaultSettings

RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"


def formatter_message(message):
    m =  message.replace(
        "$RESET", RESET_SEQ
    ).replace("$BOLD", BOLD_SEQ)
    return m


class DefaultLogger(logging.Logger):

    FORMAT = "%(levelname)s: \t%(message)s \t($BOLD%(filename)s:%(lineno)d$RESET)"
    COLOR_FORMAT = formatter_message(FORMAT)
    NONE_FORMAT = "%(levelname)s: \t%(message)s \t(%(filename)s:%(lineno)d)"

    def __init__(
        self,
        name,
        settings: DefaultSettings = None,
        log_format=None,
    ):
        super().__init__(f"{name}")
        if(settings is not None and settings.is_production()):
            if(log_format is None):
                log_format = self.NONE_FORMAT
            color_formatter = ColoredFormatter(
                log_format, 
                use_color=False
            )
            handler = watchtower.CloudWatchLogHandler(
                log_group=settings.app_name, 
                use_queues=True,
            )
            handler.setFormatter(color_formatter)
            self.addHandler(handler)
        else:
            if(log_format is None):
                log_format = self.COLOR_FORMAT
            color_formatter = ColoredFormatter(log_format)
            console = logging.StreamHandler()
            console.setFormatter(color_formatter)
            self.addHandler(console)
