import logging


cols = {
    "reset": "\033[0m",
    "white": "\033[2;39m",  # time
    "bold_green": "\033[1;32m",  # debug
    "green": "\033[0;32m",  # debug msg
    "bold_blue": "\033[1;34m",  # info
    "blue": "\033[0;34m",  # info msg
    "bold_yellow": "\033[1;33m",  # warning
    "yellow": "\033[0;33m",  # warning msg
    "bold_red": "\033[1;31m",  # error
    "red": "\033[0;31m",  # error msg
    "red_back": "\033[7;31m",  # critical
    "critic_red": "\033[1;91m",  # critical msg
    "error_msg": "\033[0;91m",
}

class CustomFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()
        
        self.FORMATS = {
            logging.DEBUG: f"{cols["white"]}%(asctime)s{cols["reset"]} | {cols["bold_green"]}%(levelname)s{cols["reset"]} | {cols["green"]}%(message)s{cols["reset"]}",
            logging.INFO: f"{cols["white"]}%(asctime)s{cols["reset"]} | {cols["bold_blue"]}%(levelname)s{cols["reset"]} | {cols["blue"]}%(message)s{cols["reset"]}",
            logging.WARNING: f"{cols["white"]}%(asctime)s{cols["reset"]} | {cols["bold_yellow"]}%(levelname)s{cols["reset"]} | {cols["yellow"]}%(message)s{cols['reset']}",
            logging.ERROR: f"{cols["white"]}%(asctime)s{cols["reset"]} | {cols["bold_red"]}%(levelname)s{cols["reset"]} | {cols["red"]}%(message)s{cols["error_msg"]}",
            logging.CRITICAL: f"{cols["white"]}%(asctime)s{cols["reset"]} | {cols["red_back"]}%(levelname)s{cols["reset"]} | {cols["critic_red"]}%(message)s{cols["reset"]}",
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)


class CustomFileFormatter(logging.Formatter):    
    def __init__(self):
        super().__init__(
            fmt='%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            style='%'
        )
    
    def format(self, record):
        if '\n' in record.msg:
            record.msg = record.msg.replace('\n', '\n\t\t| ')
        return super().format(record)


class MaxLevelFilter(logging.Filter):
    def __init__(self, max_level):
        super().__init__()
        self.max_level = max_level

    def filter(self, record):
        return record.levelno <= self.max_level


def log_exception(exception: Exception) -> str:
    """Generates a log message for caughted exception"""
    name = type(exception).__name__
    text = exception.__doc__
    log_txt = f"{name} | {text}"
    return log_txt


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# High level handler for errors and so
file_handler = logging.FileHandler("D:\\ad_sender\\logs\\error.log")
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(CustomFileFormatter())

# Low level handler for info, debug, etc
file_low_lvl = logging.FileHandler("D:\\ad_sender\\logs\\app.log")
file_low_lvl.setLevel(logging.DEBUG)
file_low_lvl.addFilter(MaxLevelFilter(logging.INFO))
file_low_lvl.setFormatter(CustomFileFormatter())

stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(CustomFormatter())

logger.addHandler(file_handler)
logger.addHandler(file_low_lvl)
logger.addHandler(stdout_handler)

# def log_uncaught_exceptions(exc_type, exc_value, exc_traceback):
#     logger.critical("lol")
#     logger.error(str(exc_value), exc_info=(exc_type, exc_value, exc_traceback))

# sys.excepthook = log_uncaught_exceptions