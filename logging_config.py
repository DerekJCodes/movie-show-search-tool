import logging
import os
from logging.handlers import RotatingFileHandler

DEFAULT_LOGGING_FILE = "reelfinder.log"

def configure_logging(log_file=DEFAULT_LOGGING_FILE, level=None):
    level_name = (level or os.getenv("LOG_LEVEL", "INFO")).upper()

    handler = RotatingFileHandler(
        log_file, maxBytes=1_000_000, backupCount=3, encoding="utf-8"
    )
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )

    root = logging.getLogger()
    root.addHandler(handler)
    root.setLevel(level_name)

    #urllib3 logs full URLs (including the API key) at DEBUG; keep it quiet.
    logging.getLogger("urllib3").setLevel(logging.WARNING)