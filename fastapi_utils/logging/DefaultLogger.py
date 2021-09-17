from .ColoredFormater import ColoredFormatter
import watchtower
import logging

RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"


def formatter_message(message, use_color=True):
    if use_color:
        message = message.replace(
            "$RESET", RESET_SEQ
        ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message

class DefaultLogger(logging.Logger):

    FORMAT = "%(levelname)s:\t%(message)s ($BOLD%(filename)s$RESET:%(lineno)d)"
    COLOR_FORMAT = formatter_message(FORMAT, True)

    def __init__(self, name, settings):
        super().__init__(f"{name}")
        if(settings.is_production()):
            handler = watchtower.CloudWatchLogHandler(log_group=settings.app_name, use_queues = False)
            self.addHandler(handler)
        else:
            color_formatter = ColoredFormatter(self.COLOR_FORMAT)
            console = logging.StreamHandler()
            console.setFormatter(color_formatter)
            self.addHandler(console)
