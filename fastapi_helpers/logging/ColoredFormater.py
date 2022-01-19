import logging

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[%dm"


class ColoredFormatter(logging.Formatter):

    COLORS = {
        'WARNING': YELLOW,
        'INFO': GREEN,
        'DEBUG': BLUE,
        'CRITICAL': MAGENTA,
        'ERROR': RED,
        'EXCEPTION': RED
    }

    def __init__(self, msg, use_color=True):
        super().__init__(msg)
        self.use_color = use_color

    def format(self, record: logging.LogRecord) -> str:
        levelname = record.levelname
        if self.use_color and levelname in self.COLORS:
            color = COLOR_SEQ % (30 + self.COLORS[levelname])
            levelname_color = f"{color}{levelname}{RESET_SEQ}:\033[10D\033[10C"
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)
